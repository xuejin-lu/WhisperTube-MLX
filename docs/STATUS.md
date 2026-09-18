# Project Status

## Current milestone

**v0.3 — End-to-end CLI pipeline**

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

## v0.2 approval

**APPROVED on 2026-09-16.**

v0.2 Local MLX transcription is closed after reviewer verification of:

- Spec Kit convergence complete with T001-T030 checked;
- requirements checklist 8/8 and security checklist 9/9 reviewed;
- deterministic tests expanded to 21 focused transcription tests and 36 full-repository tests;
- paragraph formatting now prefers sentence/punctuation boundaries near the ~500-character target and preserves content with a hard-split fallback only for pathological spans;
- local ffmpeg preflight and backend error mapping distinguish dependency, model, and audio-decode/inference failures;
- OpenCC adapter and docs use the project baseline `s2tw` configuration;
- Apple Silicon MLX smoke succeeded with `mlx-community/whisper-tiny` and produced a local ignored Markdown transcript;
- GitHub Actions passed for commit `9caff16` in run `35047914567`.

The default `mlx-community/whisper-large-v3-mlx` remains the quality target. A full large-v3 smoke was not required to close v0.2 because the milestone acceptance criteria were satisfied with the same MLX path using a smaller explicit model.

## Current milestone goal

v0.3 composes the two approved stages into one local CLI flow:

`YouTube URL -> local audio -> MLX Whisper -> Taiwan Traditional Chinese -> Markdown`

The composition must reuse the approved v0.1 acquisition and v0.2 transcription boundaries rather than duplicating their logic.

## v0.3 implementation verification

- Spec Kit artifacts, requirements checklist (10/10), security checklist (8/8), plan, contract,
  quickstart, and tasks are complete under `specs/003-end-to-end-cli/`.
- `whispertube.pipeline` composes `whispertube.youtube.main` and
  `whispertube.transcription.transcribe_audio` through injected stage seams.
- Deterministic pipeline tests cover option propagation, current-run cleanup after success/failure,
  arbitrary-path deletion protection, missing cleanup artifacts, cleanup errors, stage failure
  preservation, and CLI results.
- The full deterministic suite passes 44 tests; `compileall` and `git diff --check` pass.
- A real anonymous Apple Silicon smoke used the approved public video, yt-dlp format 251, and
  `mlx-community/whisper-tiny`. It completed in 49.38 seconds, retained one 33,165-byte Markdown
  transcript under `temp/pipeline-transcripts-v0-3/`, and left no audio file under
  `temp/pipeline-audio-v0-3/`. No human gate or browser credentials were required.

## Current blocker

None. v0.3 is ready for repository review after pushed CI verification.

## Next autonomous task

Request repository review for the v0.3 **End-to-end CLI pipeline** feature.

Codex should autonomously:

1. create a new Spec Kit feature for the end-to-end pipeline;
2. specify the one-command CLI contract and acceptance criteria;
3. define temporary audio lifecycle/cleanup behavior explicitly;
4. preserve cause-specific error boundaries so download, dependency/model/inference, and output failures remain distinguishable;
5. reuse `whispertube.youtube` and `whispertube.transcription` rather than reimplementing them;
6. add deterministic orchestration tests first (RED), using injected/fake stage boundaries so CI requires no YouTube, model download, or Apple Silicon hardware;
7. implement the minimum composition layer (GREEN), then refactor with existing v0.1/v0.2 suites still green;
8. run a real local end-to-end smoke on the approved public test video with an explicit small MLX model unless the spec justifies another safe fixture;
9. verify temporary media cleanup and that no cookie, model cache, downloaded media, or transcript is accidentally versioned;
10. run the full deterministic suite, CI, `$speckit-converge`, push, and request review.

## v0.3 scope constraints

- No GUI yet; GUI remains v0.4.
- No summarization, diarization, timestamps, batch playlists, hosted APIs, accounts, database, telemetry, or paid fallback.
- Keep all processing local except model retrieval from its documented registry when a model is not already cached.
- Preserve the existing `large-v3` default transcription target while allowing a smaller explicit model for smoke/testing.
- Do not weaken v0.1/v0.2 security/output-path/error contracts during composition.

## Known follow-up risks

- Safari browser-cookie fallback remains unexercised because anonymous YouTube acquisition succeeded in v0.1 testing.
- yt-dlp emitted a missing JavaScript-runtime warning during v0.1 smoke verification, although the approved test video downloaded successfully.
- full large-v3 runtime cost and memory use remain unmeasured; this is not a v0.3 blocker unless the end-to-end default path reveals a practical failure.
