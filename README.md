# Socratic Paimon Tutor

中文 | [English](#english)

An agent-driven tutoring system template for long-term study, role-based instruction, and persistent lesson state management.

一个面向长期学习的 Agent 家教系统模板，强调苏格拉底式教学、角色分工授课和跨会话状态延续。

## 中文

### 项目简介

`Socratic Paimon Tutor` 是一个可直接交给 Claude Code、Codex、Trae、Qoder 等 Agentic Engineering 工具接管的项目模板。

它不是普通对话提示词集合，而是一套带有状态文件、角色文档、进度记录、课后更新机制的长期陪学系统。

默认设定：

- 默认使用中文交流，除非学习者明确要求其他语言。
- 默认采用苏格拉底式教学法。
- 默认教师团队为派蒙、甘雨、刻晴。
- 默认世界观为轻度校园 AU，但教学质量优先于角色扮演。
- 默认所有成员均为清华大学计算机科学与技术和数学双学士学位项目的本科三年级学生。

### 核心特性

- 基于 `materials/` 中真实教材授课，而不是脱离材料空讲。
- 通过 `teacher/` 下的状态文件实现跨会话续学。
- 角色分工明确：派蒙负责直觉与陪伴，甘雨负责推导与耐心，刻晴负责结构与标准。
- 每节课结束后可自动维护进度、课后日记、教材修订建议和群聊状态。
- 支持轻剧情模式与弱剧情模式切换。

### 项目结构

```text
.
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── materials/
│   └── README.md
└── teacher/
    ├── system.md
    ├── system_detail.md
    ├── progress.md
    ├── learner_profile.md
    ├── paimon.md
    ├── ganyu.md
    ├── keqing.md
    ├── wechat_group.md
    ├── wechat_unread.md
    ├── diary.md
    ├── book_revision_notes.md
    └── session_archive.md
```

### 快速开始

1. 把教材、讲义、章节 Markdown、论文或 PDF 放进 `materials/`。
2. 用支持文件读写的 Agent 工具打开整个项目目录。
3. 让 Agent 先阅读 `teacher/system.md`、`teacher/system_detail.md`、`teacher/` 下其余状态文件，再扫描 `materials/`。
4. 用下面这段启动提示词接管系统。

```text
请先完整接管这个项目中的家教系统：
1. 阅读 teacher/ 下的系统文档和状态文件；
2. 扫描 materials/ 下的教材；
3. 用最少的问题完成启动校准；
4. 从现在开始，以派蒙、甘雨、刻晴组成的家教团队带我学习；
5. 默认采用苏格拉底教学法；
6. 所有对我的交流默认使用中文；
7. 每节课结束后，按系统文档要求更新相关 markdown 文件。
```

### 推荐使用方式

- 输入 `开始上课` 开始当前进度的下一段内容。
- 输入 `继续上一课` 返回上一次未完的主线。
- 输入 `今天让刻晴主讲` 直接切换主讲老师。
- 输入 `今天只讲解，不做角色演绎` 进入弱剧情模式。
- 输入 `我想看看微信群聊` 查看并消费未读群聊状态。
- 输入 `课后更新` 强制执行本节课的状态维护。

### 日常工作流

1. 将教材放入 `materials/`。
2. 启动 Agent 并完成一次初始校准。
3. 按章节或主题持续上课。
4. 每节课结束后执行课后更新。
5. 新开对话时，始终先读取 `teacher/` 状态文件再继续。

### 自定义建议

- 如果你想修改世界观，优先改 `teacher/learner_profile.md` 和 `teacher/system_detail.md`。
- 如果你想加强某位老师的风格，改对应角色文档。
- 如果你想提高严格程度，改 `teacher/system.md` 中的授课原则。
- 如果你想切换学科，只需要替换 `materials/` 中的教材，并在首次启动时重做课程校准。

### 注意事项

- 这套系统的质量高度依赖 `materials/` 的教材质量。
- 不建议把角色互动写成恋爱模拟或成人内容。
- 若要长期使用，建议定期归档 `progress.md` 和群聊日志。
- 如果你准备公开发布本仓库，建议补充 `LICENSE`、`CONTRIBUTING.md` 和版本发布说明。

### 贡献

欢迎基于此模板扩展：

- 新角色组合
- 新学科工作流
- 更严格的考试模拟机制
- 自动化教材预处理脚本

提交修改时，建议保持：

- 教学规则与角色文档分离
- 状态文件可读、可追踪、可续写
- 默认中文交互不被破坏

### 许可证

当前仓库未附带许可证文件。如果你计划公开分发，请在发布前添加合适的开源许可证。

## English

### Overview

`Socratic Paimon Tutor` is a project template for agent-driven, long-running tutoring workflows.

It is designed for tools such as Claude Code, Codex, Trae, or Qoder, and provides a persistent structure for lesson delivery, role-based tutoring, progress tracking, and post-lesson state updates.

Default assumptions:

- User-facing communication is in Chinese unless the learner explicitly requests another language.
- The default instructional method is Socratic teaching.
- The default tutor team consists of Paimon, Ganyu, and Keqing.
- The default setting is a light campus AU, while instructional quality always takes priority over roleplay.
- By default, all members are third-year undergraduates in a dual-degree program in Computer Science and Mathematics at Tsinghua University.

### Features

- Teaches from real source materials placed in `materials/`.
- Persists lesson continuity through markdown state files under `teacher/`.
- Separates tutor responsibilities across intuition, derivation, and rigor.
- Supports post-lesson updates for progress, diary entries, revision notes, and chat state.
- Allows both light-roleplay and reduced-roleplay operation modes.

### Repository Layout

```text
.
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── materials/
│   └── README.md
└── teacher/
    ├── system.md
    ├── system_detail.md
    ├── progress.md
    ├── learner_profile.md
    ├── paimon.md
    ├── ganyu.md
    ├── keqing.md
    ├── wechat_group.md
    ├── wechat_unread.md
    ├── diary.md
    ├── book_revision_notes.md
    └── session_archive.md
```

### Quick Start

1. Put textbooks, notes, papers, chapter markdown files, or PDFs into `materials/`.
2. Open the entire project folder with an agent tool that can read and update files.
3. Instruct the agent to read `teacher/system.md`, `teacher/system_detail.md`, the rest of the state files under `teacher/`, and then scan `materials/`.
4. Use the startup prompt below.

```text
Please fully take over the tutoring system in this project:
1. Read the system and state files under teacher/;
2. Scan the study materials under materials/;
3. Ask the minimum number of calibration questions;
4. Tutor me as a team consisting of Paimon, Ganyu, and Keqing;
5. Use the Socratic method by default;
6. Use Chinese for all learner-facing communication unless I ask otherwise;
7. Update the required markdown files after each lesson.
```

### Recommended Commands

- `开始上课` to start the next lesson segment
- `继续上一课` to resume the previous unfinished thread
- `今天让刻晴主讲` to switch the lead tutor
- `今天只讲解，不做角色演绎` to reduce roleplay
- `我想看看微信群聊` to inspect unread group chat state
- `课后更新` to force a post-lesson sync

### Typical Workflow

1. Add study materials to `materials/`.
2. Run the initial calibration with your agent.
3. Continue lessons over time.
4. Perform post-lesson updates after each session.
5. On every new chat, reload the `teacher/` state files before resuming.

### Customization

- Update `teacher/learner_profile.md` and `teacher/system_detail.md` to change the setting.
- Edit role files to strengthen or soften a tutor's personality.
- Adjust `teacher/system.md` if you want stricter or looser pedagogy.
- Replace the contents of `materials/` to reuse the system for a different subject.

### Notes

- System quality depends heavily on the quality and structure of the materials in `materials/`.
- This template is intended for educational roleplay, not romance simulation or adult content.
- For long-running use, archive older progress and chat logs regularly.
- If you plan to publish this repository, add a `LICENSE`, `CONTRIBUTING.md`, and release notes.

### Contributing

Extensions are welcome, especially for:

- new tutor teams
- new subject workflows
- stronger exam simulation
- automated preprocessing for study materials

When contributing, try to preserve:

- separation between teaching rules and character files
- readable and append-friendly state files
- Chinese as the default learner-facing language

### License

No license file is included yet. Add an appropriate open-source license before public distribution.
