# Project Status

## Current milestone

**v0.4 — Local graphical UI**

## v0.1 approval

**APPROVED on 2026-09-16.**

v0.1 Local YouTube audio acquisition is closed after reviewer verification of:

- Spec Kit convergence complete with 25/25 tasks checked;
- security checklist 12/12 and requirements checklist 16/16 reviewed;
- deterministic regression coverage for URL handling, CLI failures, output-path traversal, privacy contract, and downloader command construction;
- strict `yt-dlp --format bestaudio` contract aligned with FR-003;
- relative output traversal such as `temp/../../outside` rejected before downloader invocation;
- anonymous local yt-dlp smoke test succeeded with format 251 and an ignored `.webm` artifact;
- no cookie export or repository credential file was created;
- GitHub Actions passed for commit `9c68ccd` in run `35021028881`.

## v0.2 approval

**APPROVED on 2026-09-16.**

v0.2 Local MLX transcription is closed after reviewer verification of:

- Spec Kit convergence complete with T001-T030 checked;
- requirements checklist 8/8 and security checklist 9/9 reviewed;
- focused transcription tests expanded to 21 and the full repository suite to 36;
- paragraph formatting prefers sentence/punctuation boundaries near the ~500-character target and preserves content;
- ffmpeg/dependency, model, and audio-decode/inference failures are cause-specific;
- OpenCC uses the project baseline `s2tw`;
- Apple Silicon MLX smoke succeeded with `mlx-community/whisper-tiny`;
- GitHub Actions passed for commit `9caff16` in run `35047914567`.

The default `mlx-community/whisper-large-v3-mlx` remains the quality target; a full large-v3 smoke is still a later performance/compatibility check rather than a v0.2 closure requirement.

## v0.3 approval

**APPROVED on 2026-09-19.**

v0.3 End-to-end CLI pipeline is closed after reviewer verification of:

- Spec Kit convergence complete through T018;
- requirements and security checklists reviewed;
- one command composes the approved v0.1 acquisition and v0.2 transcription stages without duplicating their logic;
- temporary current-run audio is cleaned after success and transcription failure while the transcript is retained;
- cleanup never extends to arbitrary/pre-existing paths;
- simultaneous transcription failure + cleanup failure preserves the original stage category/exit code and also reports residual-audio risk;
- the default acquirer removes partial artifacts only from its dedicated current-run `run-*` directory after acquisition failure;
- focused pipeline suite passes 10 tests and the full deterministic suite passes 46 tests;
- a post-review real Apple Silicon smoke with the approved public video and `mlx-community/whisper-tiny` produced a local Markdown transcript and left the pipeline audio directory empty;
- GitHub Actions passed for remediation commit `434c0c0` in run `35402460908`;
- GitHub Actions passed for final verification commit `2d972ef` in run `35402516879`.

No v0.3 implementation blocker or Human Gate remains.

## Current milestone goal

v0.4 adds the first local graphical interface for non-technical use while reusing the approved v0.3 pipeline:

`open local app -> paste one YouTube URL -> Transcribe -> view status/preview -> save/download Markdown`

The GUI must remain a thin presentation layer over the approved pipeline rather than reimplementing acquisition or transcription.

## Next autonomous task

Use the Spec Kit lifecycle to create the v0.4 **Local Graphical UI** feature before implementation.

Codex should autonomously:

1. create a new Spec Kit feature for the local GUI;
2. research the simplest currently suitable local-only UI approach for this Apple Silicon Python project (for example Gradio or another lightweight local framework) rather than assuming a stale package/API;
3. define measurable acceptance criteria for:
   - one YouTube URL input;
   - one Start/Transcribe action;
   - visible running/success/error status;
   - transcript preview;
   - Markdown download/save;
   - preservation of v0.3 cause-specific error messages;
   - no public tunnel, hosted processing, telemetry, or account requirement;
4. reuse `whispertube.pipeline` as the orchestration boundary rather than duplicating downloader/transcription logic;
5. keep deterministic UI logic tests independent of live YouTube, model downloads, and Apple Silicon hardware;
6. run the Agent Reviewer Phase before implementation;
7. implement behavior changes with RED -> GREEN -> REFACTOR;
8. perform a real local GUI smoke on the development Mac using the approved public test video and an explicit small MLX model;
9. verify that temporary media cleanup, transcript retention, privacy boundaries, and existing v0.1-v0.3 tests remain intact;
10. run full deterministic tests, CI, `$speckit-converge`, push, and persist the review handoff in GitHub.

## v0.4 scope constraints

- Local GUI only; do not create a public share/tunnel by default.
- No hosted transcription or paid API fallback.
- No summarization, diarization, timestamps, playlist batch mode, accounts, database, or telemetry.
- Do not package a final macOS `.app` yet unless the v0.4 spec explicitly proves it is necessary; public packaging remains part of the later release milestone.
- Preserve the `large-v3` default quality target while allowing a smaller explicit model for local smoke/testing.
- Do not weaken the approved v0.1-v0.3 path, cleanup, privacy, or error contracts.

## Known follow-up risks

- Safari browser-cookie fallback remains unexercised because anonymous YouTube acquisition has succeeded in testing.
- yt-dlp has emitted a missing JavaScript-runtime warning on tested downloads, although the approved test video succeeds.
- full large-v3 runtime cost and memory use remain unmeasured.
- GUI framework choice is not yet approved and must be researched/spec-driven in v0.4.
