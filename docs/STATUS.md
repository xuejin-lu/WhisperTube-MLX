# Project Status

## Current milestone

**v0.2 — Local MLX transcription**

## v0.1 approval

**APPROVED on 2026-09-16.**

v0.1 Local YouTube audio acquisition is closed after reviewer verification of:

- Spec Kit convergence complete with 25/25 tasks checked;
- security checklist 12/12 and requirements checklist 16/16 reviewed;
- deterministic regression coverage for URL handling, CLI failures, output-path traversal, privacy contract, and downloader command construction;
- strict `yt-dlp --format bestaudio` contract aligned with FR-003;
- relative output traversal such as `temp/../../outside` rejected before downloader invocation;
- anonymous local yt-dlp smoke test succeeded on the development Mac with format `251` and an ignored `.webm` artifact;
- no cookie export or credential file was produced;
- GitHub Actions passed for commit `9c68ccd` in run `35021028881`.

The Safari/browser-cookie fallback remains intentionally unexercised because anonymous acquisition succeeded. This is a dormant fallback risk, not a v0.1 blocker.

## Current milestone goal

v0.2 must establish a local Apple Silicon transcription path:

`local audio file -> MLX-compatible Whisper -> Chinese transcript`

Do **not** connect the YouTube downloader to transcription yet. End-to-end composition belongs to v0.3.

## Next autonomous task

Use the Spec Kit lifecycle to create the v0.2 feature specification before implementation.

Codex should autonomously:

1. create a new Spec Kit feature for **Local MLX Transcription**;
2. research currently viable MLX-compatible Whisper implementations for Apple Silicon rather than assuming an old package/API;
3. define measurable acceptance criteria for:
   - local audio input;
   - Chinese transcription;
   - Apple Silicon/MLX execution;
   - preferred `large-v3` quality target where practical;
   - missing dependency/model/input error handling;
   - no cloud transcription dependency;
4. document the selected dependency and rationale in `research.md` / `plan.md`;
5. generate requirements/security-quality checklists and run the agent reviewer phase;
6. produce tasks and run `$speckit-analyze`;
7. only then begin implementation with RED → GREEN → REFACTOR;
8. run deterministic tests, local integration/smoke validation, CI, and `$speckit-converge`;
9. push and request review.

## Constraints carried forward

- Local-first and privacy-first.
- Apple Silicon Mac is the initial target.
- Free/open tooling preferred.
- No hosted transcription API.
- No GUI yet.
- No summarization, diarization, or word-level timestamps in v0.2.
- Do not modify the proven v0.1 acquisition behavior unless a v0.2 integration need exposes a real defect; if so, create a separate convergence/fix task.

## Known follow-up risks

- Safari browser-cookie fallback has not been exercised because it was not needed during v0.1 verification.
- yt-dlp emitted a missing JavaScript-runtime warning during v0.1 smoke verification, although the tested video downloaded successfully.
- Exact MLX Whisper package/API has not yet been selected and must be researched in v0.2 rather than assumed.
