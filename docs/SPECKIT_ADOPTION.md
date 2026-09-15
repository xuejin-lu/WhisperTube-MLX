# Spec Kit Adoption Plan

This repository is migrating from an ad-hoc AI workflow to **GitHub Spec Kit + Codex + TDD**.

## Goal

Make the repository itself the single source of truth so that the maintainer can normally type only:

`開始`

in Codex, and the agent can autonomously:

1. synchronize the repository;
2. read the active spec;
3. determine the next task;
4. create/update tests first;
5. implement the smallest change;
6. run validation and local smoke tests where possible;
7. update Spec Kit artifacts/status;
8. commit and push;
9. check CI;
10. return a review-ready report.

The maintainer should only be interrupted for genuine human authorization or product decisions.

## Tooling baseline

Pin the initial Spec Kit bootstrap to **v1.0.3** so the workflow is reproducible.

Codex bootstrap command for this existing repository:

```bash
uvx --from git+https://github.com/github/spec-kit.git@v1.0.3 \
  specify init --here --force --non-interactive --integration codex --script py
```

Codex should execute this itself when the required files are absent.

## Migration sequence

### Phase A — Bootstrap Spec Kit

- initialize Spec Kit in-place;
- preserve existing source, tests, README, license, and project docs;
- verify `.specify/` exists;
- verify Codex skills are installed under `.agents/skills`;
- do not delete legacy docs until their useful decisions have been migrated.

### Phase B — Create constitution

Translate stable project principles into the Spec Kit constitution:

- local-first processing;
- privacy-first handling of media and credentials;
- spec-before-code;
- mandatory TDD for behavior changes;
- reliability before UI;
- small vertical slices;
- no fake verification;
- agent-first execution / minimal human gates.

### Phase C — Migrate current product spec

Use the current `docs/PROJECT_SPEC.md` as source material to create the Spec Kit feature/spec artifacts for the active v0.1 milestone.

Do not silently change product requirements during migration.

The v0.1 feature remains:

> Reliably acquire audio from one YouTube video locally on the maintainer's Apple Silicon Mac, including a local browser-cookie fallback when anonymous access is blocked.

### Phase D — Reconcile existing implementation

The existing v0.1 implementation predates formal TDD/Spec Kit adoption.

Do not discard it merely to claim TDD purity. Instead:

1. derive acceptance tests from the migrated v0.1 spec;
2. identify gaps in the existing tests;
3. add missing tests before changing corresponding behavior;
4. run local integration/smoke verification from Codex itself;
5. use `$speckit-analyze` / `$speckit-converge` to reconcile spec, tasks, tests, and implementation;
6. only mark v0.1 complete when acceptance criteria are actually verified.

### Phase E — Add CI

GitHub Actions should run deterministic tests on every push and pull request.

CI must not:

- download real YouTube media;
- require browser cookies;
- access private media;
- rely on Apple Silicon-only MLX behavior.

Those belong to local Codex smoke/integration verification on the maintainer's Mac.

## Human gate policy

The following are **not** human tasks if Codex has shell access:

- `pip` / `uv` / Homebrew installs;
- running unit tests;
- running yt-dlp anonymously;
- inspecting output files;
- running local fixture tests;
- git fetch/rebase/commit/push;
- checking CI;
- updating docs/spec/tasks.

A human gate is justified only when Codex cannot proceed without explicit human presence or authorization, such as:

- macOS asks the user to approve Safari Keychain access;
- the user must log into YouTube in a browser;
- macOS privacy permission requires clicking a dialog;
- a product decision has multiple valid options not resolved by the spec.

When a gate occurs, Codex asks for one minimal action and then resumes automatically.

## Definition of Done for each task

A behavior-changing task is done only when:

- the relevant acceptance criterion exists in the spec;
- TDD evidence exists (RED → GREEN; REFACTOR when appropriate);
- focused tests pass;
- full deterministic suite passes;
- relevant integration/smoke test has been run by Codex when technically possible;
- spec/plan/tasks are converged;
- commit is pushed to GitHub;
- CI is green or explicitly pending with no known failure;
- the Development Report is review-ready.

## Immediate next autonomous run

On the next `開始`, Codex should **not** move to v0.2 yet.

It should:

1. pull/rebase the latest remote changes;
2. bootstrap Spec Kit v1.0.3 in-place;
3. create/migrate the constitution;
4. migrate v0.1 into Spec Kit artifacts;
5. reconcile existing v0.1 tests/implementation against the migrated spec;
6. run the real anonymous local YouTube smoke test itself;
7. if a browser-auth fallback is required, attempt the supported local path and stop only if macOS requires a human permission/login action;
8. converge v0.1;
9. commit and push all migration/verification changes;
10. return the new Spec Kit/TDD Development Report.
