# AGENTS.md

This repository is developed by one human maintainer with AI coding assistance.

## Trigger

When the user says **「開始」**, do not ask what to do next unless blocked by missing external information.

Instead:

1. Fetch and read the current repository state.
2. Read, in this order:
   - `AGENTS.md`
   - `docs/PROJECT_SPEC.md`
   - `docs/SOLO_WORKFLOW.md`
   - `docs/STATUS.md`
   - `README.md`
3. Inspect the current code and git history relevant to the next milestone.
4. Determine the smallest unfinished task from `docs/STATUS.md` that advances the current milestone.
5. Implement only that task unless a tightly coupled fix is required.
6. Run the relevant validation/tests locally.
7. Update documentation when behavior or workflow changes.
8. Update `docs/STATUS.md` with verified facts only.
9. Commit the change with a concise conventional commit message.
10. Push the commit to the configured GitHub remote so the web reviewer can inspect the exact code. If push fails because authentication, permissions, or remote setup is unavailable, stop and report that explicitly; do not claim the task is review-ready.
11. Finish with a development report containing:
    - what changed
    - files changed
    - commands/tests run and their results
    - remaining risks or blockers
    - exact next recommended task
    - commit SHA
    - push result and remote branch

## Core product rule

The main product path is:

`YouTube URL -> local audio acquisition -> local ASR on Apple Silicon -> Traditional Chinese Markdown transcript`

The app is local-first. Do not reintroduce Colab, remote Gradio tunnels, cloud cookies, hosted download proxies, or paid transcription APIs unless the spec is explicitly changed.

## Development rules

- Optimize for a single-maintainer project: simple code, small diffs, low operational burden.
- Do not over-engineer abstractions before they are needed.
- Prefer one clearly testable milestone at a time.
- Never commit cookies, browser profiles, credentials, downloaded media, private recordings, generated transcripts, or model caches.
- Treat YouTube/browser cookies as credentials.
- Do not add telemetry or upload user media anywhere by default.
- Preserve user privacy: processing should stay local unless explicitly documented otherwise.
- Do not silently change major product decisions in `docs/PROJECT_SPEC.md`.
- If a technical assumption is uncertain, verify it with a minimal experiment before building more layers on top.

## Branch / commit behavior

For normal solo development, work directly on the current development branch if one is already active. If only `main` exists and the requested environment supports branches cleanly, prefer a short-lived branch for a non-trivial milestone; otherwise keep the workflow simple and commit directly.

Use conventional commit prefixes where practical: `feat:`, `fix:`, `test:`, `docs:`, `chore:`, `refactor:`.

A task is not ready for external review until its commit is visible on the GitHub remote. A local-only commit is incomplete for this workflow.

## Stop conditions

Stop and report instead of guessing when:

- a test requires the maintainer's local browser session or macOS permission that the agent cannot access;
- YouTube behavior depends on a real local network/session and cannot be reproduced in the agent environment;
- the next step would expose credentials or private media;
- a product-level decision is missing from the spec.

When stopped, leave the repository in a clean, documented state and specify the exact command the maintainer should run locally.
