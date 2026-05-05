# Codex workflow for this TFG

## Purpose

Define how Codex/LLM assistance is used in a controlled, auditable way during the project lifecycle.

## Principles

1. **Human-led methodology**: research questions, targets, validation strategy and interpretation are decided by the student.
2. **Assistant as accelerator**: Codex helps draft code/docs/checklists, but outputs are always reviewed.
3. **Reproducibility first**: every non-trivial decision must be reflected in repository files.
4. **No hidden automation**: avoid opaque steps that cannot be traced or explained in the final report.

## Current project phase constraints

At the current stage:

- No model training.
- No data downloads committed to Git.
- No feature-engineering implementation yet.
- No experimental claims or performance results.

Codex should focus on documentation quality, repository hygiene and planning artifacts.

## Suggested interaction protocol

For each coding/documentation session:

1. State the immediate objective (e.g., "review docs consistency").
2. Ask for small, verifiable changes.
3. Run checks (formatting, tests, lint) when relevant.
4. Review diffs before committing.
5. Record methodological implications in `docs/`.

## Quality checklist before accepting LLM-generated content

- Is the text/code consistent with dataset constraints?
- Is there any potential data leakage risk?
- Are assumptions explicit and technically defensible?
- Does this conflict with earlier documented decisions?
- Can this be explained clearly in the TFG report?

## Traceability recommendations

- Keep commit messages specific and scoped.
- Link code changes to methodological notes.
- Separate refactors from scientific decisions where possible.
- Prefer incremental PRs over large mixed changes.

## Risk warnings

- LLM outputs can be plausible but wrong.
- References may be imprecise if not verified.
- Generated pipelines can accidentally leak future information.
- Overly complex solutions can reduce explainability.

## Definition of done for this phase

A change is considered complete in the current phase if it:

- improves clarity or reproducibility,
- does not introduce unvalidated scientific claims,
- does not start model implementation,
- keeps repository structure safe for future data work.
