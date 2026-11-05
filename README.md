# skill-dissector

A Claude skill that dissects *how other skills work*: trigger design, control flow, context engineering (progressive disclosure), script/judgment split, and steering style — then writes a principles report with observed-vs-inferred claims.

## Install

```bash
git clone https://github.com/xdlkc/skill-dissector ~/.claude/skills/skill-dissector
```

## Use

Ask Claude things like "拆解一下 dingtalk-todo 这个 skill 的原理" or "analyze how the skill-creator skill works".

## Layout

- `SKILL.md` — workflow and report template
- `references/analysis-framework.md` — detailed questions per layer
- `scripts/inventory.py` — structural inventory (files, frontmatter, dangling refs)
