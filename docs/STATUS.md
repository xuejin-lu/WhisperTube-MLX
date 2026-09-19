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

## v0.4 implementation review

**READY FOR REVIEW on 2026-09-19.**

v0.4 Local Graphical UI is implemented with:

- Spec Kit convergence complete through T018 with all 18 tasks checked;
- requirements checklist 13/13, security checklist 10/10, and UX checklist 10/10 reviewed;
- a pinned Gradio 6.27.0 Blocks interface that delegates exactly one request to the approved v0.3 pipeline;
- explicit loopback binding, no public share, private event APIs, strict CORS, disabled analytics/monitoring,
  and bounded transcript-file exposure;
- visible idle/running/success/error states, duplicate-run suppression, cause-specific pipeline errors,
  complete Markdown preview, and local Markdown download;
- focused GUI coverage passing 10 tests and the full deterministic repository suite passing 56 tests;
- a real local browser smoke using the approved public video and `mlx-community/whisper-tiny` that showed
  running/disabled and terminal/restored controls, produced a 33,577-byte Markdown transcript, exposed its
  preview/download, showed no public share URL, and left the current-run audio directory empty;
- GitHub Actions passing for implementation commit `3c92fd5` in run `35404368636`.

No v0.4 implementation blocker or Human Gate remains. Reviewer approval is still required before the milestone is closed.

## Next autonomous task

Review v0.4 against `specs/004-local-gui/`, the completed checklists, local smoke evidence, and exact-SHA CI.
Do not start v0.5 until v0.4 is explicitly approved or review findings are remediated and reverified.

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
- Gradio is pinned at 6.27.0; future framework upgrades require rerunning the launch/privacy contract tests and browser smoke.
