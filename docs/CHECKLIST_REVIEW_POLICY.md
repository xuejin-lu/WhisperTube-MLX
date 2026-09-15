# Spec Kit Checklist Review Policy

This project treats Spec Kit checklists as **requirements-quality review artifacts**, not as implementation task lists.

## Why this exists

Spec Kit intentionally leaves newly generated custom checklist items unchecked. The checkbox state belongs to a reviewer, and `speckit.implement` treats unchecked checklist items as a gate.

For this single-maintainer project, routine checklist review must not become a recurring human approval burden. The reviewer role is therefore agent-assisted by default.

## Pre-implementation reviewer phase

Before invoking `$speckit-implement`, Codex must run a dedicated reviewer phase that is separate from implementation work:

1. Read the active feature's `spec.md`, `plan.md`, `tasks.md`, and every file under `checklists/`.
2. Review each checklist item as a requirement-quality criterion, not as an implementation-completion item.
3. For every item that is clearly satisfied by the current requirements artifacts, mark it `[x]`.
4. For every item that is not satisfied:
   - identify the owning source artifact (`spec.md`, `plan.md`, or `tasks.md`);
   - fix the requirement/design/task artifact at the source;
   - run `$speckit-analyze` again when appropriate;
   - re-review the checklist item;
   - mark it `[x]` only after the requirement-quality criterion is actually satisfied.
5. Do **not** mark an item merely to bypass the gate.
6. Record material reviewer findings in the development report.

## Human gate criteria

Human approval is required only when the checklist item cannot be resolved from the existing product constitution/spec and instead requires one of these:

- explicit acceptance of a security/privacy risk;
- a product decision with materially different user-visible behavior;
- use or disclosure of credentials/secrets;
- a legal/licensing decision;
- an irreversible/destructive action;
- OS/browser permission that only the maintainer can grant.

If none of the above applies, the agent reviewer should resolve the checklist autonomously and continue.

## Separation of roles

The `speckit.implement` command itself must continue to treat checklist markers as read-only, consistent with Spec Kit.

Checklist updates happen in the **pre-implementation reviewer phase**, before `speckit.implement` is invoked.

For this repository, the same Codex session may perform the reviewer phase, but it must explicitly switch roles and review the requirements artifacts before implementation. When subagent/reviewer isolation is available, prefer an independent reviewer context.

## Security checklist interpretation

A generated `security.md` with unchecked items does **not** mean vulnerabilities have been found. It means the generated security requirements checklist has not yet been reviewed.

The reviewer must determine whether the requirements adequately address each criterion. Actual implementation security findings belong in tests, analysis, or code review findings, not in the mere existence of unchecked checklist boxes.

## Expected autonomous flow

```text
specify / clarify
      |
      v
plan
      |
      v
checklist + tasks
      |
      v
analyze
      |
      v
AGENT REVIEWER PHASE
- review checklist criteria
- fix source artifacts if needed
- mark satisfied criteria [x]
      |
      v
implement (TDD)
      |
      v
converge
```

The maintainer should not be asked to answer routine `yes/no` prompts merely because generated checklist boxes are still unchecked.
