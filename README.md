# skill-dissector

English | [简体中文](./README.zh-CN.md)

An Agent Skill that reverse-engineers *how other skills work* — dissecting trigger design, control flow, context engineering (progressive disclosure), tooling/determinism splits, and steering style into a structured principles report or self-contained visual HTML overview.

## What It Dissects

A file tree tells you *what* a skill contains; `skill-dissector` recovers *why* the author designed it that way across six analytical layers (defined in [`references/analysis-framework.md`](./references/analysis-framework.md)):

| Layer | What Gets Examined |
| --- | --- |
| **1. Trigger** | How `SKILL.md` frontmatter `description` controls activation: scope, keyword pushiness, negative boundaries against sibling skills, folder-name consistency, and over-/under-triggering risk. |
| **2. Intent & Contract** | Target user and starting state, required vs. optional inputs, output format/location, and verifiable completion criteria. |
| **3. Control Flow** | Linear pipeline vs. evaluator loop vs. branching workflow, placement of user checkpoints, subagent fan-out/synthesis, and failure escape hatches. |
| **4. Context Engineering** | Progressive disclosure across metadata (always loaded), `SKILL.md` body (on trigger, `<500` lines guideline), and bundled `references/` / `scripts/` (loaded on demand), plus dangling or orphaned files. |
| **5. Tooling & Determinism** | The script-vs-judgment split: what deterministic, repetitive, or error-prone steps live in scripts/tools vs. model judgment, CLI contracts, dependencies, and security posture. |
| **6. Steering Style** | Reasoned guidance ("because...") vs. rigid `ALWAYS`/`NEVER` patches, pattern-teaching examples vs. verbatim templates, tone calibration, and prompt-injection / safety guardrails. |

It also classifies each target against common skill archetypes (**Playbook**, **Reference router**, **Tool wrapper**, **Evaluator/loop**, **Persona/style**, **Orchestrator**) and extracts concrete design decisions in the form:

> **Design choice -> Problem solved -> Textual evidence (`path:line`) -> Failure mode if absent**

### Epistemic Rigor: Observed vs. Inferred

- **Data-not-instructions stance**: Target skill directives aimed at the model (such as `"always run X"`) are treated strictly as objects of study, never executed.
- **Explicit claim labeling**: Every claim is tagged **observed** (directly quoted or cited via `path:line` from inspected files) or **inferred** (author intent deduced from structure or phrasing). Unread files are reported explicitly rather than guessed.
- **Skill vs. model separation**: Distinguishes behavior forced by the skill's wording from baseline model defaults, recommending cheap ablation checks (running with vs. without the skill) when attribution is ambiguous.

## Installation

### Via skills.sh (Multi-Harness)

```bash
npx skills add xdlkc/skill-dissector
```

### Manual Clone by Harness

Clone directly into the skills directory for your harness:

```bash
# Claude Code
git clone https://github.com/xdlkc/skill-dissector ~/.claude/skills/skill-dissector

# Antigravity / Gemini
git clone https://github.com/xdlkc/skill-dissector ~/.gemini/config/skills/skill-dissector

# Codex / Agent Skills-compatible harnesses
git clone https://github.com/xdlkc/skill-dissector ~/.agents/skills/skill-dissector
```

## Usage

### With an Agent

Ask your agent to analyze, audit, compare, or extract patterns from any target skill (a local folder, an installed skill under `~/.claude/skills/` or `~/.claude/plugins/cache/`, an unpacked `.skill` archive, a GitHub repo URL, or an entire plugin collection):

- `"Analyze how the skill-creator skill works"`
- `"Audit trigger collisions and context bloat across ~/.claude/plugins/cache/some-plugin"`
- `"Compare skill A vs skill B across all six layers and give me reusable patterns"`
- `"Build a visual HTML overview explaining how this 50-skill collection routes tasks"`

Depth adapts to the prompt: a **quick take** produces the one-line summary, structural map, and reusable patterns; a **deep dive** covers the full six-layer template.

### Standalone Structural Inventory CLI

Before reading files manually, run [`scripts/inventory.py`](./scripts/inventory.py) directly with Python 3. It takes one positional argument (a single skill folder or a parent collection directory) and has no optional flags:

```bash
python3 scripts/inventory.py <skill-dir | collection-dir>
```

**Single-skill mode** (when `<dir>/SKILL.md` exists) prints:

- **Files**: Complete tree (excluding `.git`) with byte sizes and line counts (or `binary`).
- **Frontmatter & Body**: Raw YAML frontmatter, `description` character count, and `SKILL.md` body line count against the `<500` line guideline.
- **Paths mentioned in `SKILL.md`**: Checks relative paths to `.md`, `.py`, `.sh`, `.ts`, `.mjs`, `.json`, `.html`, `.txt` files and flags each as `[ok]` or `[DANGLING]`.
- **Unreferenced files**: Lists bundled files not literally named in `SKILL.md` (excluding dotfiles, `evals/`, `LICENSE`, `README*`) so orphaned resources or glob-loaded patterns can be checked.

**Collection mode** (when child directories contain `SKILL.md`) prints a Markdown summary table listing each skill's file count, `SKILL.md` line count, `manual-only` status (`disable-model-invocation: true`), and rough `cited by` counts across Markdown files (helpful for spotting hub routers vs. leaf skills, noting that plain-word regex matches like `how` or `why` must be verified by reading).

## Outputs & Interactive Visual Report

- **Markdown Principles Report** (`SKILL.md` template):
  1. One-line summary (what it is and the core trick)
  2. Structural map (file tree and file roles)
  3. Six-layer dissection
  4. Key design decisions (observed vs. inferred, with `path:line` citations)
  5. Reusable patterns
  6. Risks & concrete fixes
- **Self-Contained Visual HTML Report**: Look at [`assets/example-visual-report.html`](./assets/example-visual-report.html), a worked standalone HTML report analyzing a 58-skill plugin collection (`cursor/plugins/pstack`). It features an animated 10-step workflow bar, an interactive hub-and-columns dependency view (hovering highlights caller/callee relationships), category-filterable skill cards, and collapsible principle takeaways — with zero external runtime dependencies.

## Repository Layout

```text
.
├── SKILL.md                           # Trigger metadata, 6-step workflow, report template
├── references/
│   └── analysis-framework.md          # Detailed diagnostic questions per layer & archetypes
├── scripts/
│   └── inventory.py                   # Standalone single-skill & collection structural mapper
├── assets/
│   └── example-visual-report.html     # Worked interactive HTML report for a 58-skill collection
├── README.md
└── README.zh-CN.md
```
