#!/usr/bin/env python3
"""课程分支 + 全局主干记忆管理器。"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


@dataclass
class MergePolicy:
    min_confidence: float = 0.7
    min_unique_courses: int = 1
    min_occurrences: int = 2

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "MergePolicy":
        return cls(
            min_confidence=float(raw.get("min_confidence", 0.7)),
            min_unique_courses=int(raw.get("min_unique_courses", 1)),
            min_occurrences=int(raw.get("min_occurrences", 2)),
        )


class BranchMemoryManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.global_path = base_dir / "global_memory.json"
        self.candidates_path = base_dir / "global_candidates.json"
        self.policy_path = base_dir / "merge_policy.json"
        self.journal_path = base_dir / "learning_journal.json"

    def init_storage(self) -> None:
        write_json(
            self.global_path,
            {
                "updated_at": utc_now(),
                "entries": {},
            },
        )
        write_json(self.candidates_path, {"updated_at": utc_now(), "items": []})
        write_json(
            self.policy_path,
            {
                "min_confidence": 0.7,
                "min_unique_courses": 1,
                "min_occurrences": 2,
            },
        )
        write_json(self.journal_path, {"updated_at": utc_now(), "events": []})

    def add_journal_event(self, event: Dict[str, Any]) -> None:
        payload = read_json(self.journal_path, {"updated_at": utc_now(), "events": []})
        payload["events"].append({"at": utc_now(), **event})
        payload["updated_at"] = utc_now()
        write_json(self.journal_path, payload)

    def add_course_note(self, course: str, key: str, value: str, confidence: float) -> Path:
        course_path = self.base_dir / "courses" / course / "memory.json"
        raw = read_json(course_path, {"updated_at": utc_now(), "entries": {}})
        raw["entries"][key] = {
            "value": value,
            "confidence": confidence,
            "updated_at": utc_now(),
        }
        raw["updated_at"] = utc_now()
        write_json(course_path, raw)
        self.add_journal_event(
            {
                "type": "course_note_added",
                "course": course,
                "key": key,
                "confidence": confidence,
            }
        )
        return course_path

    def set_course_meta(self, course: str, book: str, status: str, summary: str = "") -> Path:
        meta_path = self.base_dir / "courses" / course / "meta.json"
        payload = read_json(meta_path, {})
        payload.update(
            {
                "course": course,
                "book": book,
                "status": status,
                "summary": summary,
                "updated_at": utc_now(),
            }
        )
        write_json(meta_path, payload)
        self.add_journal_event(
            {
                "type": "course_status_changed",
                "course": course,
                "status": status,
            }
        )
        return meta_path

    def add_global_candidate(
        self,
        course: str,
        key: str,
        value: str,
        confidence: float,
        session: str,
    ) -> None:
        payload = read_json(self.candidates_path, {"updated_at": utc_now(), "items": []})
        payload["items"].append(
            {
                "course": course,
                "key": key,
                "value": value,
                "confidence": confidence,
                "session": session,
                "created_at": utc_now(),
            }
        )
        payload["updated_at"] = utc_now()
        write_json(self.candidates_path, payload)
        self.add_journal_event(
            {
                "type": "global_candidate_added",
                "course": course,
                "key": key,
                "session": session,
            }
        )

    def merge(self) -> Dict[str, Any]:
        policy = MergePolicy.from_dict(read_json(self.policy_path, {}))
        global_memory = read_json(self.global_path, {"updated_at": utc_now(), "entries": {}})
        candidates = read_json(self.candidates_path, {"updated_at": utc_now(), "items": []})

        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for item in candidates["items"]:
            grouped.setdefault(item["key"], []).append(item)

        merged = []
        rejected = []

        for key, items in grouped.items():
            top = sorted(items, key=lambda i: i["confidence"], reverse=True)[0]
            unique_courses = {i["course"] for i in items}
            max_conf = max(i["confidence"] for i in items)
            enough = (
                len(items) >= policy.min_occurrences
                and len(unique_courses) >= policy.min_unique_courses
                and max_conf >= policy.min_confidence
            )
            if enough:
                global_memory["entries"][key] = {
                    "value": top["value"],
                    "confidence": max_conf,
                    "source_sessions": sorted({i["session"] for i in items}),
                    "source_courses": sorted(unique_courses),
                    "last_validated": utc_now(),
                }
                merged.append(key)
            else:
                rejected.append(key)

        global_memory["updated_at"] = utc_now()
        write_json(self.global_path, global_memory)

        retained = [item for item in candidates["items"] if item["key"] in rejected]
        write_json(self.candidates_path, {"updated_at": utc_now(), "items": retained})

        self.add_journal_event(
            {
                "type": "merge_executed",
                "merged": merged,
                "rejected": rejected,
            }
        )

        return {
            "merged": merged,
            "rejected": rejected,
            "policy": {
                "min_confidence": policy.min_confidence,
                "min_unique_courses": policy.min_unique_courses,
                "min_occurrences": policy.min_occurrences,
            },
        }

    def simulate_learning_flow(self, reset: bool = False) -> Dict[str, Any]:
        if reset and self.base_dir.exists():
            shutil.rmtree(self.base_dir)

        self.init_storage()

        # 1) 输入书籍并建课
        self.set_course_meta("linear_algebra", "线性代数讲义（第3版）", "active")
        self.set_course_meta("probability", "概率论与数理统计基础", "active")

        # 2) 多轮课程学习与课后更新
        self.add_course_note("linear_algebra", "proof_rigor", "证明细节耐心提升", 0.68)
        self.add_global_candidate(
            "linear_algebra",
            "pacing_preference",
            "先例子再定义",
            0.72,
            "2026-03-10-s01",
        )

        self.add_course_note("probability", "error_pattern", "条件概率中事件方向常写反", 0.81)
        self.add_global_candidate(
            "probability",
            "pacing_preference",
            "先例子再定义",
            0.76,
            "2026-03-12-s02",
        )

        merge_result = self.merge()

        # 3) 结课
        self.set_course_meta(
            "linear_algebra",
            "线性代数讲义（第3版）",
            "completed",
            "完成矩阵论、特征值与二次型，证明能力提升明显。",
        )
        self.set_course_meta(
            "probability",
            "概率论与数理统计基础",
            "completed",
            "完成条件概率、随机变量与分布，计算稳定性提升。",
        )

        global_entries = read_json(self.global_path, {"entries": {}}).get("entries", {})
        return {
            "base_dir": str(self.base_dir),
            "courses": ["linear_algebra", "probability"],
            "global_keys": sorted(global_entries.keys()),
            "merge_result": merge_result,
            "journal": str(self.journal_path),
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="课程分支与全局记忆管理工具")
    parser.add_argument("--base-dir", default="teacher/memory", help="存储目录")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="初始化存储文件")

    p_course = sub.add_parser("add-course-note", help="记录课程分支记忆")
    p_course.add_argument("--course", required=True)
    p_course.add_argument("--key", required=True)
    p_course.add_argument("--value", required=True)
    p_course.add_argument("--confidence", type=float, default=0.6)

    p_candidate = sub.add_parser("add-global-candidate", help="添加候选全局记忆")
    p_candidate.add_argument("--course", required=True)
    p_candidate.add_argument("--key", required=True)
    p_candidate.add_argument("--value", required=True)
    p_candidate.add_argument("--confidence", type=float, required=True)
    p_candidate.add_argument("--session", required=True)

    sub.add_parser("merge", help="按策略合并到全局记忆")

    p_sim = sub.add_parser("simulate-flow", help="模拟从输入书籍到结课的完整流程")
    p_sim.add_argument(
        "--reset",
        action="store_true",
        help="执行前清空 base-dir（仅用于演示）",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()
    manager = BranchMemoryManager(Path(args.base_dir))

    if args.command == "init":
        manager.init_storage()
        print(f"初始化完成: {args.base_dir}")
        return

    if args.command == "add-course-note":
        path = manager.add_course_note(
            course=args.course,
            key=args.key,
            value=args.value,
            confidence=args.confidence,
        )
        print(f"已写入课程记忆: {path}")
        return

    if args.command == "add-global-candidate":
        manager.add_global_candidate(
            course=args.course,
            key=args.key,
            value=args.value,
            confidence=args.confidence,
            session=args.session,
        )
        print("已写入候选全局记忆")
        return

    if args.command == "merge":
        result = manager.merge()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.command == "simulate-flow":
        result = manager.simulate_learning_flow(reset=args.reset)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
