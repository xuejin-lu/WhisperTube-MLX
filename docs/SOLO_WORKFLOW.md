# Solo Development Workflow

This project is intentionally optimized for one maintainer using AI coding agents.

## 1. Roles

### Maintainer

The human maintainer:

- decides product direction;
- runs tests that require the real Mac, browser session, microphone/media, or local network;
- reviews Codex reports;
- reports unexpected behavior back to the reviewing assistant.

### Codex

Codex is the implementation agent.

When told **「開始」**, Codex should read `AGENTS.md` and the project docs, determine the next smallest unfinished task, implement it, validate it, commit it, and return a concise report.

### Review assistant

The review assistant:

- reads Codex's development report;
- can inspect the GitHub repository directly;
- checks whether the implementation matches the spec;
- identifies regressions, over-engineering, missing tests, security issues, and incorrect assumptions;
- updates the spec/status/workflow when product decisions change.

## 2. One-task loop

Use this loop repeatedly:

```text
Maintainer says 「開始」 in Codex
        |
        v
Codex reads repo + STATUS
        |
        v
Codex selects smallest useful task
        |
        v
Implement + test + commit
        |
        v
Codex returns development report
        |
        v
Maintainer pastes report into review chat
        |
        v
Review assistant checks repo/code/results
        |
        +--> approved -> next 「開始」
        |
        +--> changes needed -> review assistant writes exact correction task
```

Do not batch many milestones into one coding session.

## 3. Task sizing

A good Codex task should normally satisfy one of these:

- one capability;
- one bug fix;
- one testable refactor;
- one documentation/workflow update tightly coupled to a code change.

Avoid tasks such as:

- "build the whole app";
- "finish v1.0";
- "add downloader + Whisper + UI + packaging".

Prefer:

- "add URL normalization with tests";
- "add a downloader wrapper around yt-dlp";
- "add local Safari cookie fallback";
- "wire one local audio file into the selected MLX Whisper API".

## 4. Verification levels

Use the cheapest verification level that proves the change.

### Level A — Static/unit verification

Examples:

- URL parsing tests;
- filename/output formatting;
- subprocess argument generation;
- error classification;
- Markdown formatting.

Codex should run these itself.

### Level B — Dependency/integration verification

Examples:

- yt-dlp binary discovery;
- ffmpeg discovery;
- import selected MLX package;
- local fixture transcription.

Codex should run these if its environment supports them.

### Level C — Maintainer-local verification

Required when behavior depends on:

- the maintainer's Mac hardware;
- Apple Silicon acceleration;
- Safari/Chrome cookies;
- residential IP / YouTube anti-bot behavior;
- macOS privacy/security permissions.

Codex must not pretend Level C passed. It should provide the exact command and expected evidence for the maintainer to run.

## 5. Git workflow

Keep Git simple.

For each coherent task:

1. inspect current `git status`;
2. make the smallest required diff;
3. run validation;
4. update `docs/STATUS.md` only with verified facts;
5. commit once the task is coherent.

Suggested commit forms:

- `feat: add YouTube URL normalization`
- `feat: add local yt-dlp downloader`
- `fix: handle YouTube authentication errors`
- `test: cover playlist URL normalization`
- `docs: record local verification result`

Do not commit generated media or credentials.

## 6. Status discipline

`docs/STATUS.md` is the project handoff state.

It should answer:

- current milestone;
- what is verified;
- what is not yet verified;
- current blocker;
- exact next task;
- any maintainer-local command awaiting results.

Do not turn `STATUS.md` into a diary. Keep only current, decision-relevant state.

## 7. Codex development report format

Every Codex run should finish with this structure:

```markdown
# Development Report

## Result
<one-sentence outcome>

## Changes
- ...

## Files changed
- `path`: purpose

## Validation
- `command` -> PASS/FAIL

## Local verification needed
- None

or

- Run: `...`
- Expected evidence: `...`

## Risks / blockers
- ...

## Next recommended task
<exactly one task>

## Commit
`<sha> <message>`
```

The maintainer can paste this report directly into the review chat.

## 8. Review policy

A review should focus on:

1. correctness against `PROJECT_SPEC.md`;
2. whether tests actually prove the claim;
3. privacy/security, especially cookies and local media;
4. unnecessary complexity;
5. whether the next task is still the smallest sensible step.

Do not refactor working code merely for style during early milestones unless it prevents testing or creates a real maintenance risk.

## 9. Release discipline

Do not publish a release merely because code exists.

A version is release-worthy only after its milestone acceptance criteria are verified on the maintainer's actual Apple Silicon Mac where required.
