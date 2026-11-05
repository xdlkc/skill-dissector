# Analysis framework (detailed questions per layer)

## Contents
1. Trigger  2. Intent & contract  3. Control flow  4. Context engineering  5. Tooling & determinism  6. Steering style  7. Common archetypes

## 1. Trigger
- Does the description state both *what* it does and *when* to use it? All "when" info belongs in frontmatter because the body loads only after triggering.
- Is it deliberately "pushy" (lists many phrasings, says "even if the user doesn't name X") to counter under-triggering?
- Are there negative boundaries ("does not do Y, use Z") that prevent collisions with sibling skills?
- Is it so broad it will hijack unrelated tasks? So narrow it misses paraphrases or other languages?
- Is `name` consistent with the folder, and is the description a reasonable length?

## 2. Intent & contract
- Who is the intended user and what is their starting state?
- Inputs required/optional; output format (fixed template vs. free-form); where outputs are saved.
- What does "done" look like? Is it verifiable?

## 3. Control flow
- Linear pipeline, loop-until-satisfied, or branching by variant?
- Human checkpoints (questions, review steps) and why they sit where they do.
- Parallelism / subagents: what is fanned out, how results merge, how baselines or verifiers are used.
- Failure handling and escape hatches.

## 4. Context engineering
- Three levels: metadata (always loaded) → SKILL.md body (on trigger) → bundled files (on demand). Which content sits at which level?
- Does SKILL.md point to references with clear "read when…" conditions? Any dangling or orphaned files?
- Size: body under ~500 lines? Long references have a table of contents?
- Variant organization (one reference per framework/domain) so only the relevant one is read.

## 5. Tooling & determinism
- What is scripted (repetitive, deterministic, error-prone) vs. left to judgment?
- Do scripts have clear CLI contracts, error messages, and no hidden side effects (network, deletion)?
- Required binaries/MCP servers/permissions; what happens if absent.
- Security posture: does it execute downloaded content, write outside its workspace, handle secrets?

## 6. Steering style
- Reasoned guidance ("because…") vs. rigid ALWAYS/NEVER. Heavy caps usually signal a past failure the author patched.
- Concrete examples and templates: do they teach a pattern or risk being copied verbatim?
- Tone calibration to user expertise; language handling.
- Guardrails: safety stance, prompt-injection awareness, scope limits.

## 7. Common archetypes (to name what you see)
- **Playbook**: ordered steps for a procedure (deploy, release).
- **Reference router**: thin SKILL.md dispatching to per-domain docs.
- **Tool wrapper**: instructions around a CLI/API with scripts.
- **Evaluator/loop**: draft → test → measure → revise (e.g. skill-creator).
- **Persona/style**: shapes voice or taste; hard to verify objectively.
- **Orchestrator**: coordinates subagents/workflows.
A skill is often a hybrid; name the dominant one and the secondary.
