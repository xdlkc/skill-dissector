# skill-dissector

[English](./README.md) | 简体中文

一个用于拆解*其他 Agent Skill 工作原理*的元技能（Meta-Skill）：从触发机制、控制流、上下文工程（渐进式披露）、脚本与模型判断边界、到提示词引导风格进行六层剖析，并输出区分“已观测”与“推断”的结构化原理报告或交互式单文件 HTML 全景图。

## 拆解维度

文件目录只能看出一个 skill **有什么**，而 `skill-dissector` 重点还原作者**为什么这样设计**。完整诊断清单见 [`references/analysis-framework.md`](./references/analysis-framework.md)，涵盖六个层次：

| 层次 | 分析内容 |
| --- | --- |
| **1. 触发机制（Trigger）** | 检查 `SKILL.md` frontmatter 的 `description` 如何决定激活时机：覆盖范围、主动触发话术（pushiness）、与兄弟技能的负向边界、目录名一致性及误触/漏触风险。 |
| **2. 意图与契约（Intent & Contract）** | 目标用户与前置状态、必选/可选输入、输出形态与落盘位置，以及可验证的完成判据。 |
| **3. 控制流（Control Flow）** | 线性流水线、评估-改进循环还是分支路由；人工确认卡点的位置合理性；子代理并发与汇总方式；异常兜底路径。 |
| **4. 上下文工程（Context Engineering）** | 三级渐进式披露（常驻元数据 → 触发后加载的 `SKILL.md` 正文 → 按需读取的 `references/` 与 `scripts/`）、正文 `<500` 行体量控制、引用条件清晰度以及悬空/孤立文件检查。 |
| **5. 工具与确定性（Tooling & Determinism）** | 确定性脚本与模型主观判断的切分（repetitive/易错逻辑是否下沉到脚本）、CLI 契约与报错质量、依赖项及安全边界。 |
| **6. 引导风格（Steering Style）** | 讲道理式引导（`because...`）与刚性 `ALWAYS`/`NEVER` 补丁的权衡、示例教学与死模板风险、语气匹配及防提示词注入护栏。 |

同时会识别技能所属原型（**Playbook 剧本型**、**Reference router 参考路由型**、**Tool wrapper 工具封装型**、**Evaluator/loop 评估循环型**、**Persona/style 风格人设型**、**Orchestrator 编排器型**），并按以下结构提炼关键设计决策：

> **设计选择 → 解决的问题 → 文本证据（`path:line`）→ 缺席时的失效模式**

### 严谨性原则：Observed vs. Inferred

- **数据视角而非指令视角**：分析目标 skill 中的模型指令（例如 `"always run X"`）只作研究对象描述，绝不顺带执行其流程。
- **严格区分观测与推断**：每条结论必须标注 **observed**（有文件原文或 `path:line` 依据）或 **inferred**（基于结构与措辞推导的作者意图）；未读取的文件会明确列出，不作猜测。
- **剥离技能文本与模型默认能力**：区分哪些行为真正来自 `SKILL.md` 约束、哪些源自模型自身默认倾向，必要时建议做对照实验（启用 vs 禁用该 skill）。

## 安装方式

### 通过 skills.sh 安装（多运行环境）

```bash
npx skills add xdlkc/skill-dissector
```

### 按运行环境手动克隆

```bash
# Claude Code
git clone https://github.com/xdlkc/skill-dissector ~/.claude/skills/skill-dissector

# Antigravity / Gemini
git clone https://github.com/xdlkc/skill-dissector ~/.gemini/config/skills/skill-dissector

# Codex / 兼容 Agent Skills 规范的环境
git clone https://github.com/xdlkc/skill-dissector ~/.agents/skills/skill-dissector
```

## 使用方法

### 在 Agent 中调用

可直接提供本地技能路径、`~/.claude/skills/` 或 `~/.claude/plugins/cache/` 下的技能名、`.skill` 压缩包、GitHub 仓库链接或整个插件集合目录：

- `"拆解一下 dingtalk-todo 这个 skill 的原理"`
- `"审计 ~/.claude/plugins/cache/某插件 下各技能的触发冲突与上下文膨胀"`
- `"按六层框架横向对比 skill A 与 skill B，提炼可复用设计模式"`
- `"生成一个普通人一眼看懂的 HTML 可视化报告，讲清楚这组 skill 是怎么协作的"`

输出深度可按需求自动调整：**快速概览**仅输出一句话总结、结构地图与可复用模式；**深度剖析**则输出完整六段报告。

### 独立运行结构盘点脚本

在通读文件之前，可直接通过 Python 3 运行 [`scripts/inventory.py`](./scripts/inventory.py)。脚本只接收一个位置参数（单个技能目录或技能集合父目录），无额外 CLI 选项：

```bash
python3 scripts/inventory.py <skill-dir | collection-dir>
```

**单技能模式**（目标目录包含 `SKILL.md`）输出：

- **Files**：完整文件清单（自动跳过 `.git`）、字节大小与行数（二进制文件标注 `binary`）。
- **Frontmatter & Body**：YAML frontmatter 原文、`description` 字符数，以及正文行数（对照 `<500` 行基线）。
- **Paths mentioned in `SKILL.md`**：提取正文中引用的相对路径（`.md` / `.py` / `.sh` / `.ts` / `.mjs` / `.json` / `.html` / `.txt`），并检查磁盘存在性，标记 `[ok]` 或 `[DANGLING]`。
- **Unreferenced files**：列出未被 `SKILL.md` 显式点名的文件（排除隐藏文件、`evals/`、`LICENSE`、`README*`），用于排查孤立文件或通配符按需加载模式。

**集合模式**（子目录包含 `SKILL.md`）输出 Markdown 汇总表：展示每个技能的文件数、`SKILL.md` 行数、是否仅手动触发（`disable-model-invocation: true`）以及在集合内其他 `.md` 文件中被提及次数（`cited by`），用于快速识别枢纽路由技能与叶子技能（注：计数基于普通词边界正则匹配，若技能名包含常见词如 `how`、`why`，需通读原文确认真实调用关系）。

## 报告形式与交互式可视化示例

- **Markdown 原理报告**（见 [`SKILL.md`](./SKILL.md) 模板）：
  1. 一句话总结（核心定位与关键巧思）
  2. 结构地图（文件树与各文件职责）
  3. 六层拆解（触发 · 意图 · 控制流 · 上下文 · 工具 · 引导）
  4. 关键设计决策（标注 observed / inferred 及 `path:line` 引用）
  5. 可复用模式
  6. 风险与改进建议
- **单文件交互式 HTML 报告**：仓库内置 [`assets/example-visual-report.html`](./assets/example-visual-report.html)，展示了针对 `cursor/plugins/pstack`（58 个 skill）的完整可视化拆解案例：包含 10 步自动播放总流程、枢纽与分栏调用关系图（悬停高亮上下游调用）、按分类筛选的技能卡片以及可展开查看的 24 条工程原则，零外部运行时依赖，浏览器直接打开即可查看。

## 仓库结构

```text
.
├── SKILL.md                           # 触发元数据、六步分析流程与报告模板
├── references/
│   └── analysis-framework.md          # 六层诊断问题清单与七类常见技能原型
├── scripts/
│   └── inventory.py                   # 独立单技能/技能集合结构盘点 CLI
├── assets/
│   └── example-visual-report.html     # 58 个 skill 集合的交互式 HTML 原理报告示例
├── README.md
└── README.zh-CN.md
```
