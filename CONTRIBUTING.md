# Contributing

感谢你为 `Socratic Paimon Tutor` 做贡献！

## 提交前检查

1. 保持 `teacher/system.md` 与 `teacher/system_detail.md` 的规则一致性。
2. 若修改了教学流程，请同步更新 `README.md` 与相关 `teacher/*.md` 状态说明。
3. 避免引入与当前状态不一致的历史描述（例如已删除工具的命令示例）。
4. 提交前至少运行：
   - `git diff --check`

## Commit 建议

- 使用清晰的动词开头标题，例如：
  - `Refine README open-source sections`
  - `Add course registry documentation`

## Pull Request 建议

PR 描述建议包含：

- **Why**：为什么改
- **What changed**：改了什么文件、行为
- **Validation**：做了哪些检查

## 范围建议

- 与教学状态相关的改动，优先小步提交，便于追踪。
- 不相关的大规模格式化请单独提交。
