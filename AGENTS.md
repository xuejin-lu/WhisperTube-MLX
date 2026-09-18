# AGENTS.md

This repository uses **GitHub Spec Kit + Codex + test-driven development (TDD)**.
The human maintainer should not be used as a command runner for mechanical development work.

## Trigger: 「開始」

When the user says **「開始」**, execute the development loop autonomously. Do not ask the maintainer to run ordinary shell commands, tests, downloads, installs, git commands, or local smoke tests that Codex can run itself.

### 0. Synchronize safely

1. Inspect `git status`.
2. Preserve any existing user work; never discard uncommitted changes.
3. Fetch the configured remote.
4. If the working tree is clean, rebase the current branch on its remote tracking branch before starting.
5. Read the latest repository instructions after synchronization.

### 1. Ensure Spec Kit is installed for Codex

This project is migrating to GitHub Spec Kit, pinned initially to **v1.0.3**.

If `.specify/` and the Codex Spec Kit skills are not present, bootstrap the existing repository yourself:

```bash
# Prefer uv/uvx. If uv is missing and Homebrew is available, install uv first.
uvx --from git+https://github.com/github/spec-kit.git@v1.0.3 \
  specify init --here --force --non-interactive --integration codex --script py
```

Do not ask the maintainer to type this command unless Codex genuinely cannot execute local shell commands.

After initialization, use the Codex Spec Kit skills installed under `.agents/skills`.

### 2. Use the Spec Kit lifecycle

For a new or materially changed feature, follow the Spec Kit lifecycle instead of ad-hoc coding:

1. `$speckit-constitution` — only when project principles are missing or intentionally changed.
2. `$speckit-specify` — WHAT and WHY, with measurable acceptance criteria.
3. `$speckit-clarify` — when meaningful ambiguity exists.
4. `$speckit-plan` — HOW, architecture, dependencies, test strategy.
5. `$speckit-checklist` — quality gates for non-trivial work.
6. `$speckit-tasks` — small ordered tasks.
7. `$speckit-analyze` — cross-check spec/plan/tasks before implementation.
8. **Agent reviewer phase** — review and resolve all generated checklist items according to `docs/CHECKLIST_REVIEW_POLICY.md`. Routine unchecked checklist items are not a human approval gate.
9. `$speckit-implement` — implement tasks using TDD below.
10. `$speckit-converge` — compare implementation to spec and append/fix remaining tasks.
11. Repeat implement/converge until converged.

Do not call `$speckit-implement` while generated checklist items remain unchecked unless a real human gate defined in `docs/CHECKLIST_REVIEW_POLICY.md` is unresolved.

For a tiny bug fix, use the smallest appropriate Spec Kit bug/feature path; do not create ceremony that is larger than the change.

## TDD is mandatory for behavior changes

For each behavior-changing task:

1. **RED** — add or update the smallest automated test that expresses the next acceptance criterion; run it and confirm it fails for the expected reason.
2. **GREEN** — implement the minimum code needed to make that test pass.
3. **REFACTOR** — improve structure only if useful, with the suite staying green.
4. Run the relevant focused tests, then the full automated suite.

Do not write implementation first and backfill tests afterward unless the task is explicitly investigative/spike work. If a spike is needed, keep it out of the final implementation or convert its learning into tests before shipping.

### Test layers

- **Unit tests:** pure parsing, command construction, formatting, error classification.
- **Integration tests:** local dependency behavior such as yt-dlp invocation, file creation, ffmpeg discovery, MLX imports.
- **Local smoke/e2e tests:** real YouTube acquisition and later real MLX transcription on the maintainer's Mac.
- **CI tests:** deterministic tests that do not require browser credentials, private media, or unstable external YouTube access.

## Agent-first execution policy

Codex must execute mechanical work itself whenever technically possible, including:

- installing project/development dependencies;
- running unit/integration/full test suites;
- running local yt-dlp smoke tests;
- inspecting generated files and logs;
- running format/lint/static checks;
- reviewing Spec Kit checklists and fixing source artifacts;
- updating specs/plans/tasks/status documentation;
- persisting review-relevant facts in GitHub before handoff, especially `docs/STATUS.md`, active Spec Kit tasks/checklists, and commit/CI state;
- committing, rebasing, and pushing changes;
- checking CI results when available.

### Human gates are exceptional

Ask the maintainer only when an action fundamentally requires human presence or authorization, for example:

- approving a macOS Keychain/privacy dialog;
- logging into a browser account;
- granting an OS permission;
- making a product decision not determined by the spec;
- handling a secret that must never be exposed to the agent/repository;
- explicitly accepting a material security/privacy/legal risk.

Unchecked generated checklist items by themselves are **not** a human gate. Follow `docs/CHECKLIST_REVIEW_POLICY.md` first.

When a human gate is necessary, ask for **one minimal action**, not a list of shell commands. After approval, Codex resumes the workflow itself.

## Product constitution principles

Until the formal Spec Kit constitution is generated, these rules are binding:

1. **Local-first:** YouTube acquisition, ASR, post-processing, and transcript generation run locally on Apple Silicon Mac.
2. **Privacy-first:** never upload media, cookies, browser profiles, transcripts, or credentials by default.
3. **Spec before implementation:** acceptance criteria precede code for meaningful changes.
4. **TDD:** behavior changes follow RED → GREEN → REFACTOR.
5. **Reliability before UI:** validate each pipeline stage before wrapping it in GUI layers.
6. **Small vertical slices:** implement the smallest independently verifiable behavior.
7. **No fake verification:** never mark hardware/network/browser-dependent behavior verified unless Codex actually ran it on the local machine or a documented human gate was completed.
8. **No unnecessary human labor:** the maintainer reviews decisions and exceptional permissions; the agent performs routine engineering operations.

## Git and CI

- Keep commits coherent and reviewable.
- Use conventional prefixes where practical: `feat:`, `fix:`, `test:`, `docs:`, `chore:`, `refactor:`.
- Never commit cookies, browser profiles, credentials, downloaded media, private recordings, generated private transcripts, or model caches.
- Push completed commits to the configured GitHub remote.
- A task is not review-ready until its commit is visible remotely.
- CI must remain green for deterministic tests before declaring a task complete.
- If remote changed concurrently, fetch/rebase safely instead of asking the maintainer to resolve a routine non-conflicting divergence.

## Current-state instruction

Read `docs/STATUS.md`, the active Spec Kit feature, `docs/SPECKIT_ADOPTION.md`, and `docs/CHECKLIST_REVIEW_POLICY.md` before implementation. Do not rely on a hard-coded historical milestone in this file; `docs/STATUS.md` and the active feature artifacts define the current work.

## Review handoff

GitHub is the canonical handoff between Codex and the review assistant.

Before declaring a run review-ready, Codex must:

1. update `docs/STATUS.md` with the active milestone, verified facts, unresolved risks/blockers, and the exact review state;
2. update the active Spec Kit tasks/checklists/spec as required;
3. commit and push all reviewable code and documentation;
4. verify deterministic CI and record the relevant commit/run in repository state when useful.

The maintainer must **not** be required to copy/paste the Development Report into ChatGPT. After Codex finishes, the maintainer may simply tell the review assistant **「review」** / **「檢查 GitHub」**. The review assistant then inspects the pushed repository directly.

Because this chat is not automatically notified by GitHub pushes, one short review trigger from the maintainer is still required unless a separate notification automation is configured.

## Development report

Finish each autonomous run with the following report for the Codex UI / human convenience. This report is **not** a required transport mechanism to the review assistant; all facts needed for review must already be persisted in GitHub:

```markdown
# Development Report

## Spec
- active spec / feature
- acceptance criteria addressed

## Checklist review
- checklist files reviewed
- requirements defects found/fixed
- unresolved human-gate items, if any

## TDD evidence
- RED: test(s) added and expected failure observed
- GREEN: implementation and passing focused tests
- REFACTOR: any cleanup performed

## Changes
- ...

## Validation
- focused tests -> PASS/FAIL
- full test suite -> PASS/FAIL
- integration/smoke tests -> PASS/FAIL/SKIPPED with reason
- CI -> PASS/FAIL/PENDING

## Human gate
- None
```

If a real human gate exists, replace `None` with exactly one minimal requested action.

Then include:

```markdown
## Spec Kit convergence
- CONVERGED / NOT CONVERGED
- remaining tasks, if any

## Risks / blockers
- ...

## Git
- commit SHA and message
- pushed branch

## Next action
- exactly one next autonomous task, or `Review requested`
```
