#!/usr/bin/env python3
"""Print a structural inventory of a skill directory.

Usage: inventory.py <skill-dir>
Reports file tree with sizes/line counts, SKILL.md frontmatter, body length,
relative paths mentioned in SKILL.md, and dangling/orphaned files.
"""
import re
import sys
from pathlib import Path


def collection(root):
    """Summarize a directory whose children are skills (plugin / marketplace)."""
    skills = sorted(d for d in root.iterdir()
                    if d.is_dir() and (d / "SKILL.md").is_file())
    texts = {d.name: (d / "SKILL.md").read_text(encoding="utf-8")
             for d in skills}
    # include playbooks/references so hub skills get credit for what they route to
    full = {n: "\n".join(f.read_text(encoding="utf-8", errors="ignore")
                         for f in (root / n).rglob("*.md"))
            for n in texts}
    print(f"# Collection: {root.name}  ({len(skills)} skills)\n")
    print("| skill | files | SKILL.md lines | manual-only | cited by |")
    print("|---|---|---|---|---|")
    for n in texts:
        files = sum(1 for f in (root / n).rglob("*") if f.is_file())
        lines = len(texts[n].splitlines())
        manual = "disable-model-invocation: true" in texts[n]
        pat = re.compile(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])")
        cited = sorted(m for m in full if m != n and pat.search(full[m]))
        print(f"| {n} | {files} | {lines} | {'yes' if manual else 'no'} | "
              f"{len(cited)}: {', '.join(cited[:6])}{'...' if len(cited) > 6 else ''} |")
    print("\nHubs = skills with many outgoing mentions; leaves = cited but "
          "cite little. Verify each edge by reading before claiming it.")


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: inventory.py <skill-dir | collection-dir>")
    root = Path(sys.argv[1]).expanduser().resolve()
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        if root.is_dir() and any((d / "SKILL.md").is_file()
                                 for d in root.iterdir() if d.is_dir()):
            return collection(root)
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
        r"(?<![\w.-])[\w-]+/[\w.-]+\.(?:md|py|sh|ts|mjs|json|html|txt)", body))
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
    print("\n## Files not literally named in SKILL.md "
          "(may still be reached via a pattern such as playbooks/<title>.md)")
    print("\n".join(f"- {o}" for o in orphan) or "(none)")


if __name__ == "__main__":
    main()
