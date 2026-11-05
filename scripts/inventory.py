#!/usr/bin/env python3
"""Print a structural inventory of a skill directory.

Usage: inventory.py <skill-dir>
Reports file tree with sizes/line counts, SKILL.md frontmatter, body length,
relative paths mentioned in SKILL.md, and dangling/orphaned files.
"""
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: inventory.py <skill-dir>")
    root = Path(sys.argv[1]).expanduser().resolve()
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        sys.exit(f"error: {skill_md} not found (is this a skill directory?)")

    files = sorted(p for p in root.rglob("*")
                   if p.is_file() and ".git" not in p.parts)
    print(f"# Inventory: {root.name}\n\n## Files")
    for p in files:
        rel = p.relative_to(root)
        try:
            lines = len(p.read_text(encoding="utf-8").splitlines())
            info = f"{lines} lines"
        except (UnicodeDecodeError, OSError):
            info = "binary"
        print(f"- {rel}  ({p.stat().st_size} B, {info})")

    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    print("\n## Frontmatter")
    if m:
        fm, body = m.group(1), m.group(2)
        print(fm)
        desc = re.search(r"^description:\s*(.*)$", fm, re.M)
        if desc:
            print(f"\n(description length: {len(desc.group(1))} chars)")
    else:
        body = text
        print("MISSING or malformed frontmatter")
    print(f"\n## Body\n{len(body.splitlines())} lines (guideline: <500)")

    mentioned = set(re.findall(
        r"(?:scripts|references|assets|agents|templates)/[\w./-]+", body))
    mentioned = {s.rstrip(".,)`'\"") for s in mentioned}
    print("\n## Paths mentioned in SKILL.md")
    for s in sorted(mentioned):
        status = "ok" if (root / s).exists() else "DANGLING"
        print(f"- {s}  [{status}]")

    others = {str(p.relative_to(root)) for p in files} - {"SKILL.md"}
    orphan = [o for o in sorted(others)
              if not any(o == s or o.startswith(s.rstrip("/") + "/")
                         for s in mentioned)
              and not o.startswith((".", "evals", "LICENSE", "README"))]
    print("\n## Files not referenced from SKILL.md")
    print("\n".join(f"- {o}" for o in orphan) or "(none)")


if __name__ == "__main__":
    main()
