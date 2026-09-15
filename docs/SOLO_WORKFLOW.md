# Solo Development Workflow

This project is optimized for one human maintainer using Codex as the primary implementation agent and this repository as the source of truth.

The workflow is **Spec Kit + TDD + CI + agent-first execution**.

## 1. Roles

### Maintainer

The human maintainer:

- decides product direction when the specification does not already decide it;
- grants exceptional OS/browser permissions when a human action is truly required;
- reviews development reports and final product behavior;
- does **not** act as the routine shell-command runner.

### Codex

Codex is the implementation and local verification agent.

When told **「開始」**, Codex should:

1. synchronize the repository safely;
2. read `AGENTS.md` and Spec Kit artifacts;
3. identify the current feature and next task;
4. use the Spec Kit lifecycle;
5. follow TDD for behavior changes;
6. run tests/integration/smoke checks itself when technically possible;
7. update spec/plan/tasks/status artifacts;
8. commit and push;
9. check CI;
10. return a review-ready report.

### Review assistant

The review assistant:

- inspects the pushed GitHub code directly;
- checks implementation against the spec and tests;
- detects regressions, over-engineering, security/privacy issues, and false verification claims;
- updates workflow/spec guidance when needed.

## 2. Normal loop

```text
Maintainer says 「開始」 in Codex
        |
        v
Codex syncs repo
        |
        v
Spec Kit: specify/plan/tasks/analyze as needed
        |
        v
TDD: RED -> GREEN -> REFACTOR
        |
        v
Codex runs unit + integration + local smoke tests
        |
        v
Spec Kit converge
        |
        v
Commit + push
        |
        v
GitHub Actions CI
        |
        v
Codex returns Development Report
        |
        v
Maintainer pastes report into review chat
        |
        v
Review assistant inspects pushed code
        |
        +--> approved -> next 「開始」
        |
        +--> changes needed -> repo guidance/spec updated
```

The maintainer should not be asked to run routine `git`, `python`, `pytest/unittest`, `yt-dlp`, `ffmpeg`, package install, or smoke-test commands if Codex has shell access.

## 3. Spec-driven development

Use GitHub Spec Kit as the canonical feature workflow.

For meaningful feature work:

1. constitution/principles
2. specification (WHAT/WHY + acceptance criteria)
3. clarification when needed
4. implementation plan (HOW)
5. checklist/quality gates for non-trivial changes
6. ordered tasks
7. analysis/cross-artifact consistency check
8. implementation
9. convergence against the spec

Do not let `docs/STATUS.md` become a substitute for a real feature specification.

## 4. TDD discipline

For every behavior-changing task:

### RED

Write the smallest automated test expressing the next acceptance criterion and confirm it fails for the expected reason.

### GREEN

Implement the minimum behavior required to make it pass.

### REFACTOR

Clean structure only when useful while keeping the suite green.

Then run:

- focused tests;
- full deterministic suite;
- applicable integration/smoke verification.

Existing pre-TDD code should be reconciled by deriving acceptance tests from the spec before further behavior changes. Do not rewrite working code merely to manufacture historical RED evidence.

## 5. Verification levels

### Automated unit verification

Codex always runs these itself.

Examples:

- URL parsing;
- filename/output formatting;
- subprocess argument construction;
- error classification;
- Markdown formatting.

### Local integration verification

Codex runs these itself on the development Mac when available.

Examples:

- yt-dlp binary discovery and execution;
- ffmpeg discovery;
- real local file creation;
- MLX import/model loading;
- fixture transcription.

### Local smoke/e2e verification

Codex should also run real local smoke tests itself when shell/network access exists.

Examples:

- real YouTube audio acquisition over the Mac's current network;
- end-to-end local transcription;
- temporary-file cleanup.

### Human authorization gate

A human step is justified only if the OS/service requires explicit human presence or credentials, for example:

- approving Safari/Keychain access;
- logging into YouTube interactively;
- granting macOS privacy permission;
- choosing between unresolved product alternatives.

Ask for one minimal action, then resume autonomous execution.

## 6. CI policy

GitHub Actions runs deterministic tests on push/pull request.

CI should not depend on:

- live YouTube availability;
- browser cookies;
- private media;
- Apple Silicon-specific MLX execution.

Those are covered by Codex-local integration/smoke verification.

A pushed task is not complete if deterministic CI is known to be failing.

## 7. Git policy

Codex owns routine repository mechanics:

1. inspect working tree;
2. fetch remote;
3. safely rebase clean local work when needed;
4. make the smallest coherent change;
5. validate;
6. commit;
7. push;
8. check CI.

Do not ask the maintainer to resolve a routine non-conflicting divergence.

Never commit generated media, browser cookies, credentials, private transcripts, or model caches.

## 8. Development report

The canonical report format is defined in `AGENTS.md` and must include:

- active spec and acceptance criteria addressed;
- RED/GREEN/REFACTOR evidence;
- changes;
- validation and smoke-test evidence;
- CI status;
- human gate (normally `None`);
- Spec Kit convergence status;
- risks/blockers;
- pushed commit/branch;
- exactly one next action or `Review requested`.

## 9. Release discipline

Do not publish a release because code merely exists.

A release is justified only after the relevant Spec Kit acceptance criteria are converged, deterministic CI is green, and required local Mac integration/e2e behavior has actually been verified.
