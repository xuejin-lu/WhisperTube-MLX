---

description: "Implementation tasks for local audio input"
---

# Tasks: Local Audio Input

**Input**: Design documents from `/specs/006-local-media-input/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/ui.md`, `quickstart.md`

**Tests**: Required by the feature specification and repository TDD constitution. Every behavior-changing test task is RED before its corresponding implementation task.

## Phase 1: Setup

**Purpose**: Establish the feature-specific test and documentation touch points without changing product behavior.

- [x] T001 [P] Add local-audio test imports, backend fakes, and source-byte fixture helpers in `tests/test_gui.py`.
- [x] T002 [P] Verify the non-sensitive smoke fixture and runtime output paths remain ignored in `.gitignore`, updating `.gitignore` only if a required pattern is absent.

## Phase 2: Foundational

**Purpose**: Define the shared request-dispatch seam before story-specific implementation.

- [x] T003 [P] Add a request-selection test matrix in `tests/test_gui.py` covering URL-only, local-only, neither, and both inputs with exact backend-call assertions per `contracts/ui.md`.
- [x] T004 [P] Add deterministic GUI safety tests in `tests/test_gui.py` for local source path handling, sanitized unexpected path-containing exceptions, and unchanged existing loopback/privacy configuration.

## Phase 3: User Story 1 — Transcribe a local audio file (Priority: P1) 🎯 MVP

**Goal**: Choose one supported local audio file and receive the existing validated Taiwan Traditional Chinese Markdown result without invoking yt-dlp.

**Independent Test**: Mock `transcribe_audio()` and `run_pipeline()`, submit local-only input for every approved suffix, and prove exactly one local call, no pipeline call, and a validated preview/download result.

### Tests for User Story 1 (RED first)

- [x] T005 [P] [US1] Add local-only dispatch tests in `tests/test_gui.py` proving `transcribe_audio()` receives the selected filepath, model, and output directory while `run_pipeline()` is not called.
- [x] T006 [P] [US1] Add approved-suffix and unsupported-suffix tests in `tests/test_gui.py`/`tests/test_transcription.py` proving local video containers fail as input before inference.
- [x] T007 [P] [US1] Add local transcript preview/download byte-identity tests in `tests/test_gui.py` using a validated Markdown artifact.

### Implementation for User Story 1

- [x] T008 [US1] Implement the mutually exclusive request dispatcher in `whispertube/gui.py`, routing URL-only requests to `run_pipeline()` and local-only requests to `transcribe_audio()` without duplicating canonical validation.
- [x] T009 [US1] Add the single-file local audio component and one-action event wiring in `whispertube/gui.py`, preserving private queued execution and existing running/terminal state transitions.
- [x] T010 [US1] Preserve the existing transcript validation and result exposure path in `whispertube/gui.py` for both input routes, including safe output errors.

**Checkpoint**: Local audio and YouTube URL requests are independently dispatchable, mutually exclusive, and produce the existing validated result shape.

## Phase 4: User Story 2 — Preserve the original file (Priority: P1)

**Goal**: Keep the user's original local audio present and byte-identical across all local transcription outcomes.

**Independent Test**: Use a temporary source fixture and mocked local transcription outcomes for success, inference failure, and output failure; compare bytes and existence before/after and assert no cleanup/backend pipeline call touches the source.

### Tests for User Story 2 (RED first)

- [x] T011 [P] [US2] Add success-path source ownership tests in `tests/test_gui.py` proving the selected local audio remains present and byte-identical after local transcription.
- [x] T012 [P] [US2] Add inference-failure, output-failure, and simulated cancellation/interruption ownership tests in `tests/test_gui.py` proving the source remains unchanged and no YouTube cleanup path runs.
- [x] T013 [P] [US2] Add same-stem output collision tests in `tests/test_gui.py`/`tests/test_transcription.py` proving existing transcripts are never silently overwritten.

### Implementation for User Story 2

- [x] T014 [US2] Map local `TranscriptionError` categories to safe GUI terminal states in `whispertube/gui.py` without deleting, moving, renaming, truncating, or overwriting the source.
- [x] T015 [US2] Reuse and, if needed, minimally harden the existing canonical local input/output boundaries in `whispertube/transcription.py` so all seven suffixes and collision behavior remain deterministic without weakening the CLI.

**Checkpoint**: The user's original local file is unchanged after success and representative failure paths, and output collisions are explicit errors.

## Phase 5: User Story 3 — Keep YouTube behavior unchanged (Priority: P1)

**Goal**: Add local audio without weakening the approved YouTube pipeline, privacy settings, or GUI usability.

**Independent Test**: Run the existing GUI/pipeline regression suite, inspect the generated Gradio configuration, and perform a local smoke for both the URL and local route boundaries without public sharing.

### Tests for User Story 3 (RED first)

- [x] T016 [P] [US3] Extend `tests/test_gui.py` component/configuration assertions for the local file label, single-file configuration, accepted suffix metadata, one visible Transcribe action, and private event wiring.
- [x] T017 [P] [US3] Extend `tests/test_gui.py` privacy regression coverage to prove unrelated direct file routes remain denied and ambient `GRADIO_ALLOWED_PATHS` remains rejected.
- [x] T018 [P] [US3] Add URL-only regression assertions in `tests/test_gui.py` proving existing trimming, pipeline invocation, result validation, error categories, and YouTube behavior remain unchanged.

### Implementation for User Story 3

- [x] T019 [US3] Update `README.md` with the normal URL-or-local-audio workflow, supported audio suffixes, local-video exclusion, and source ownership/privacy expectations.
- [x] T020 [US3] Preserve or refactor `whispertube/gui.py` event wiring so loopback-only launch, no share URL, strict CORS, disabled analytics/monitoring, one-active-job behavior, and stale-result clearing remain intact.

**Checkpoint**: Existing YouTube behavior and v0.4 privacy/file-serving boundaries remain green while local audio is available through the same UI.

## Phase 6: Polish and Cross-Cutting Validation

**Purpose**: Validate the complete feature, record evidence, and prepare the review handoff without publishing a release.

- [x] T021 [P] Run `specs/006-local-media-input/quickstart.md` deterministic scenarios and `git diff --check`; record any required adjustments in `docs/STATUS.md`.
- [x] T022 Run a real Apple Silicon local-audio GUI smoke with `mlx-community/whisper-tiny` and a non-sensitive untracked fixture; verify non-empty Markdown, unchanged source bytes, no yt-dlp acquisition, loopback-only binding, and no public share URL.
- [x] T023 [P] Inspect tracked/reviewable artifacts with `whispertube.release.inspect_artifacts` and verify no source audio, transcript, model cache, credential, cookie, or absolute local path is included.
- [x] T024 Run `$speckit-converge` for feature 006, append and implement any remaining traceable tasks, then rerun focused/full tests until converged.
- [x] T025 Update `docs/STATUS.md` with feature 006 evidence, exact commit/CI state, unresolved risks, and the explicit no-new-release boundary.
- [x] T026 Commit and push the converged feature, verify exact-HEAD deterministic CI, and stop for repository review.

## Dependencies & Execution Order

- Phase 1 and Phase 2 precede all user stories.
- US1 establishes the dispatcher and shared local result path; US2 depends on that route; US3 depends on US1/US2 to prove regression safety.
- Within each story, tests are written and observed RED before implementation tasks.
- Phase 6 depends on all three stories and must complete before commit/push handoff.

## Parallel Opportunities

- T001 and T002 can run in parallel.
- T003 and T004 can run in parallel before dispatcher implementation.
- T005–T007 are independent RED tests in the same test module and can be designed together, but implementation follows them sequentially because they share `gui.py` behavior.
- T011–T013 and T016–T018 are independent test cases that can be added together before their respective implementation tasks.
- T021 and T023 can run in parallel after implementation; T022 requires the local Apple Silicon runtime.

## Implementation Strategy

1. Complete setup/foundation and observe the dispatch tests fail for the missing local route.
2. Deliver US1 as the MVP: local-only dispatch plus the existing result validation.
3. Add US2 ownership/error guarantees without changing the transcription engine.
4. Add US3 UI/documentation/regression coverage.
5. Run smoke, converge, full validation, commit/push, and request review.
