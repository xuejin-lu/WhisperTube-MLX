---

description: "Implementation tasks for the downloader-only product pivot"
---

# Tasks: Downloader-Only Pivot

**Input**: Design documents from `/specs/007-downloader-only-pivot/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/downloader.md, quickstart.md

**Tests**: Every behavior-changing implementation task follows RED → GREEN → REFACTOR.

## Phase 1: Setup and active-scope migration

- [x] T001 Update `.specify/feature.json` to point at `specs/007-downloader-only-pivot` and verify the Spec Kit prerequisite scripts resolve feature 007.
- [x] T002 [P] Rewrite `requirements-macos.txt` to the pinned yt-dlp-only runtime dependency and remove the obsolete UI requirements file from the active setup path.
- [x] T003 [P] Update `scripts/setup_macos.sh` and `scripts/launch_macos.sh` for a downloader-only venv, project-managed yt-dlp PATH, paths with spaces, and non-destructive reruns.
- [x] T004 [P] Add executable `DownloadAudio.command` that invokes the project-managed downloader, prompts for one URL, and never starts a browser or server.

## Phase 2: Deterministic tests first (RED)

- [x] T005 Add `tests/test_downloader.py` URL classification tests for watch, youtu.be, Shorts, live, embed, explicit playlist, watch-plus-list, invalid host, invalid scheme, and malformed IDs; run them and record the expected RED failure before implementation.
- [x] T006 Add command-construction tests for video and playlist requests, deterministic output templates, `bestaudio`, playlist continuation, no-playlist protection, no MP3 conversion, and explicit-only cookie arguments.
- [x] T007 Add runner/summary tests with a fake streaming yt-dlp process covering completion markers, skipped/error reporting, non-zero exit propagation, missing executable, and no shell interpolation.
- [x] T008 Add launcher/setup subprocess tests for a project path containing spaces, project-owned yt-dlp discovery with a clean PATH, argument preservation, missing venv, and no GUI/transcription invocation.
- [x] T009 Add active-scope regression tests proving the normal module and launcher do not import or invoke MLX, Whisper, OpenCC, Gradio, the old pipeline, or a localhost server.

## Phase 3: Core downloader implementation (GREEN)

- [x] T010 Implement `RequestKind`, `DownloadRequest`, and URL classification/normalization in `whispertube/downloader.py` according to the downloader contract.
- [x] T011 Implement safe argv construction for video and explicit playlist requests, including output templates, `bestaudio`, playlist continuation flags, and optional browser cookies.
- [x] T012 Implement output-root preparation and a streaming yt-dlp runner that preserves yt-dlp progress, counts completion/error markers, prints the final summary, and returns the authoritative process status.
- [x] T013 Implement the downloader CLI prompt/argument parser, actionable missing-dependency and invalid-input errors, and the no-transcription normal entry point.

**Checkpoint**: Focused downloader tests pass and both video/playlist command contracts are deterministic.

## Phase 4: Active mainline simplification

- [x] T014 Remove the obsolete active GUI, pipeline, transcription, release-diagnostic, and old `whispertube.youtube` modules, `WhisperTube.command`, and their superseded tests from current mainline; retain historical access through Git history/tag v1.0.0.
- [x] T015 Update CI to run the downloader-only deterministic suite without installing UI/MLX dependencies.
- [x] T016 Update `README.md` first-screen documentation around `DownloadAudio.command`, manual Colab upload, output paths, cookie opt-in, and downloader troubleshooting; remove current-workflow transcription/GUI instructions.
- [x] T017 Update `docs/STATUS.md` to record the 007 pivot, removed active dependencies, historical v1.0.0 boundary, and no-new-release rule.

## Phase 5: Integration and smoke validation

- [x] T018 [P] Run the focused downloader tests, full deterministic suite, `git diff --check`, and shell syntax/executable checks.
- [x] T019 [P] Run a real single-video smoke with the approved public test video and a safe temporary output root; verify exactly one non-MP3 audio artifact, no transcript, no server, and no committed media.
- [x] T020 [P] Run a real small-playlist smoke with a safe temporary output root; verify multiple numerically ordered audio files, continuation/reporting behavior, and no transcription invocation.
- [x] T021 [P] Inspect tracked artifacts for credentials, cookies, media, transcripts, model caches, and absolute local paths.
- [x] T022 Run `$speckit-converge` for feature 007, append any remaining traceable tasks, implement them, and rerun validation until converged.

## Phase 6: Review handoff

- [ ] T023 Update `docs/STATUS.md` with exact test/smoke/artifact evidence, unresolved risks, exact commit/CI state, and explicit no-new-release boundary.
- [ ] T024 Commit and push the converged downloader-only pivot, verify exact-HEAD deterministic CI, confirm a clean tree, and stop for repository review.

## Dependencies & Execution Order

- Phase 1 precedes all tests.
- T005–T009 are RED tests and must be run before T010–T013 implementation.
- T010–T013 precede removal of obsolete active modules in T014.
- T018–T021 depend on the implementation and migration phases; T022 follows all of them.
- T023–T024 are the final handoff tasks and do not publish a new release.

## Parallel Opportunities

- T002–T004 can proceed in parallel after T001.
- T005–T009 can be authored together, then run as one RED checkpoint.
- T018–T021 can proceed in parallel after T017, subject to the real smoke tests sharing only ignored temporary output.
