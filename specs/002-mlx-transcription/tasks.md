---
description: "Implementation tasks for local MLX transcription"
---

# Tasks: Local MLX Transcription

**Input**: Design documents from `/specs/002-mlx-transcription/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli.md, quickstart.md

**Tests**: Required by the constitution and v0.2 specification. Every behavior change follows RED
→ GREEN → REFACTOR; deterministic tests use injected fakes, while real MLX work is local-only.

## Phase 1: Setup

**Purpose**: Declare the local inference dependencies without adding platform-only packages to CI.

- [X] T001 Add pinned local macOS inference dependencies and CI boundary comments in `requirements-macos.txt`
- [X] T002 Add the v0.2 module entry point and public CLI invocation scaffold in `whispertube/transcription.py`

## Phase 2: Foundational

**Purpose**: Establish shared validation, adapter, and error boundaries before user-story behavior.

- [X] T003 [P] Create deterministic fake backend/converter test fixtures and test module setup in `tests/test_transcription.py`
- [X] T004 [P] Define input, output, model, and transcription failure categories in `whispertube/transcription.py`
- [X] T005 [P] Document v0.2 local transcript and model-cache ignore expectations in `.gitignore` and `docs/PROJECT_SPEC.md`

**Checkpoint**: The isolated transcription boundary and deterministic test seams are ready; `whispertube/youtube.py` remains unchanged.

## Phase 3: User Story 1 - Transcribe Local Audio to Chinese Markdown (Priority: P1) 🎯 MVP

**Goal**: Turn one readable local audio file into one non-empty UTF-8 Taiwan Traditional Chinese Markdown artifact.

**Independent Test**: Inject a fake MLX result for a local fixture path and verify one Markdown artifact,
correct metadata, UTF-8 text, local conversion, and no hosted call.

### Tests for User Story 1 (write first and confirm RED)

- [X] T006 [P] [US1] Add RED tests for valid local input, exactly-one Markdown output, UTF-8 encoding, readable paragraph formatting, and ignored output path in `tests/test_transcription.py`
- [X] T007 [P] [US1] Add RED tests for explicit Chinese transcription configuration and Taiwan Traditional conversion in `tests/test_transcription.py`

### Implementation for User Story 1

- [X] T008 [US1] Implement regular-file/readability validation, normalized ignored output validation, and single-artifact naming in `whispertube/transcription.py`
- [X] T009 [US1] Implement the lazy MLX Whisper adapter, OpenCC conversion boundary, readable paragraph formatter, and Markdown renderer in `whispertube/transcription.py`
- [X] T010 [US1] Implement the successful CLI/library path with explicit `language=zh` and `task=transcribe` in `whispertube/transcription.py`

**Checkpoint**: US1 works with injected dependencies and produces one local Markdown transcript.

## Phase 4: User Story 2 - Use Apple Silicon MLX Locally (Priority: P2)

**Goal**: Select the large-v3 quality target by default while supporting an explicit smaller model for constrained local smoke runs.

**Independent Test**: Inject a fake backend and verify default/override model references and MLX call arguments without downloading weights.

### Tests for User Story 2 (write first and confirm RED)

- [X] T011 [P] [US2] Add RED tests for the default `mlx-community/whisper-large-v3-mlx`, explicit model override, and MLX backend invocation in `tests/test_transcription.py`

### Implementation for User Story 2

- [X] T012 [US2] Implement model configuration, lazy `mlx_whisper.transcribe` import, and local model-reference handling in `whispertube/transcription.py`
- [X] T013 [US2] Add the documented Apple Silicon setup, small-model smoke command, and model-cache privacy guidance in `README.md` and `specs/002-mlx-transcription/quickstart.md`
- [X] T014 [US2] Run a real short local MLX transcription smoke test with an explicit small model and record model, output, timing, and human-gate facts in `docs/STATUS.md`

**Checkpoint**: US1 remains independent, and US2 has a documented real local MLX verification path.

## Phase 5: User Story 3 - Report Transcription Failures Clearly (Priority: P3)

**Goal**: Distinguish invalid input, missing dependency, model, inference, and output failures with actionable non-zero exits.

**Independent Test**: Trigger each failure with injected fakes or temporary paths and verify no success artifact is reported.

### Tests for User Story 3 (write first and confirm RED)

- [X] T015 [P] [US3] Add RED tests for missing/non-file/unreadable input, missing dependency, model/load failure, inference/no-text failure, and cause-specific exit codes in `tests/test_transcription.py`
- [X] T016 [P] [US3] Add RED tests for unsafe/unwritable/colliding output paths and no-overwrite behavior in `tests/test_transcription.py`

### Implementation for User Story 3

- [X] T017 [US3] Implement cause-specific exception mapping, actionable CLI messages, and exit codes 2–6 in `whispertube/transcription.py`
- [X] T018 [US3] Ensure failure paths do not create or overwrite transcript artifacts and keep runtime paths local in `whispertube/transcription.py`

**Checkpoint**: All v0.2 failure categories are deterministic, actionable, and independently tested.

## Phase 6: Polish and Cross-cutting Verification

**Purpose**: Reconcile artifacts, run all required validation, and deliver a review-ready commit.

- [X] T019 [P] Update v0.2 usage, scope boundaries, and verified local behavior in `README.md`, `docs/STATUS.md`, and `specs/002-mlx-transcription/quickstart.md`
- [X] T020 Run focused transcription tests, the full deterministic suite, `compileall`, and `git diff --check` from the repository root
- [X] T021 Inspect ignored runtime/model paths for credentials, media, caches, and generated transcripts before commit in the repository root
- [X] T022 Run `$speckit-converge` against the v0.2 spec, plan, tasks, constitution, implementation, and tests; append any remaining work to this file
- [X] T023 Push the coherent v0.2 commit and verify deterministic GitHub Actions CI is green before requesting review

## Dependencies and Execution Order

- Phase 1 has no dependencies.
- Phase 2 depends on Phase 1 and blocks all user stories.
- US1 depends on Phase 2 and is the MVP.
- US2 depends on Phase 2 but does not modify or compose the v0.1 downloader.
- US3 depends on the shared boundaries from Phase 2 and can be completed after US1.
- Phase 6 depends on the desired user stories and must complete before review.

### Parallel Opportunities

- T003, T004, and T005 can proceed in parallel because they touch separate test, source, and documentation files.
- T006 and T007 can proceed in parallel only before implementation tasks touch the same test file.
- T011 can be written independently of T006/T007 once the test harness exists.
- T015 and T016 can be written in parallel before T017/T018.
- T019 and T021 touch separate documentation/inspection concerns.

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational phases.
2. Complete US1 with fake backend tests first.
3. Validate the isolated local transcript contract.
4. Add US2 real MLX smoke and US3 failure hardening.

### TDD Rule

For each behavior-changing task, add the smallest failing test, run it to capture RED, implement the
minimum GREEN change, then refactor only while focused and full suites remain green.

### Scope Guard

Do not connect the YouTube downloader to transcription in v0.2. Do not add GUI, hosted APIs,
summarization, diarization, timestamps, or cloud telemetry.
