# Tasks: End-to-End CLI Pipeline

**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/cli.md`

## Phase 1: Setup

- [X] T001 Create `whispertube/pipeline.py` module scaffold and pipeline runtime ignore coverage in `.gitignore`
- [X] T002 Create injected-stage test harness in `tests/test_pipeline.py`

## Phase 2: Foundational

- [X] T003 Define pipeline request, error categories, temporary-root validation, and cleanup ownership in `whispertube/pipeline.py`

## Phase 3: User Story 1 - One-command transcript (P1)

**Independent Test**: Fake stages receive URL/audio/model/output options and return one transcript path.

- [X] T004 [US1] Add RED composition/option propagation/CLI success tests in `tests/test_pipeline.py`
- [X] T005 [US1] Implement acquisition-to-transcription orchestration and CLI in `whispertube/pipeline.py`

## Phase 4: User Story 2 - Safe temporary audio lifecycle (P2)

**Independent Test**: Current-run audio is removed after success and transcription failure; unrelated paths survive.

- [X] T006 [US2] Add RED cleanup ownership, success, failure, missing-file, and cleanup-error tests in `tests/test_pipeline.py`
- [X] T007 [US2] Implement guarded finally-path cleanup in `whispertube/pipeline.py`

## Phase 5: User Story 3 - Cause-specific errors (P3)

**Independent Test**: Inject stage failures and assert category/exit preservation and no forbidden next-stage call.

- [X] T008 [US3] Add RED download and propagated transcription failure/CLI exit tests in `tests/test_pipeline.py`
- [X] T009 [US3] Implement download wrapping, transcription propagation, cleanup exit handling in `whispertube/pipeline.py`

## Phase 6: Verification

- [X] T010 Update `README.md`, `docs/PROJECT_SPEC.md`, `docs/STATUS.md`, and `specs/003-end-to-end-cli/quickstart.md`
- [X] T011 Run focused/full tests, static checks, real small-model public-video smoke, artifact inspection, and `$speckit-converge`
- [X] T012 Push and verify CI before requesting review

## Dependencies

T001–T003 precede all user stories. T004 precedes T005; T006 precedes T007; T008 precedes T009.
T010–T012 follow all stories. All behavior changes require RED → GREEN → REFACTOR.
