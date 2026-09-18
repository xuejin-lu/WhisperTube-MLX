# Tasks: Local Graphical UI

**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/ui.md`

**Tests**: Mandatory RED → GREEN → REFACTOR for every behavior change.

## Phase 1: Setup

- [X] T001 Add pinned Gradio dependency in `requirements-ui.txt` and deterministic CI installation in `.github/workflows/test.yml`
- [X] T002 Create the local GUI module scaffold in `whispertube/gui.py` and test scaffold in `tests/test_gui.py`

## Phase 2: Foundational

- [X] T003 Define GUI status/result data boundaries and injected pipeline callable types in `whispertube/gui.py`
- [X] T004 Define explicit local-only Blocks, queue, event, and launch configuration constants in `whispertube/gui.py`

## Phase 3: User Story 1 - Transcribe One Video Without Terminal (P1) 🎯 MVP

**Goal**: One URL and one action start exactly one approved pipeline run with visible running state.

**Independent Test**: Inject a fake pipeline and prove blank input is rejected, valid input is trimmed and
propagated once, stale values clear on start, and duplicate pending submissions are disabled by the event contract.

- [X] T005 [US1] Add RED request-validation, one-call propagation, running-state, and stale-clearing tests in `tests/test_gui.py`
- [X] T006 [US1] Implement framework-independent request handling and running-state adaptation in `whispertube/gui.py`
- [X] T007 [US1] Add RED Gradio component/event wiring tests for labeled URL input, Transcribe action, visible status, and one-active-event settings in `tests/test_gui.py`
- [X] T008 [US1] Implement the Gradio Blocks layout and chained running-to-terminal event in `whispertube/gui.py`

## Phase 4: User Story 2 - Understand Success and Failure (P2)

**Goal**: Success and every failure type produce safe, actionable, cause-specific status.

**Independent Test**: Inject each approved pipeline exception and an unexpected exception, then verify category,
message, terminal state, cleared result fields, and absence of traceback/sensitive detail.

- [X] T009 [US2] Add RED success, approved-error, unexpected-error, and sensitive-traceback suppression tests in `tests/test_gui.py`
- [X] T010 [US2] Implement terminal status and error adaptation while preserving approved pipeline categories in `whispertube/gui.py`
- [X] T011 [US2] Add RED local-only construction and launch configuration tests for loopback, share, telemetry, monitoring, CORS, file roots, and API exposure in `tests/test_gui.py`
- [X] T012 [US2] Implement local-only queue and launch behavior plus CLI configuration in `whispertube/gui.py`

## Phase 5: User Story 3 - Preview and Save Markdown (P3)

**Goal**: A successful validated transcript has exact preview/download content; unsafe results are rejected.

**Independent Test**: Use local transcript fixtures covering valid, outside-root, missing, empty, unreadable,
invalid-UTF-8, and wrong-suffix paths and compare successful preview bytes with the source artifact.

- [X] T013 [US3] Add RED transcript-root/type/content validation and byte-equivalent preview/download tests in `tests/test_gui.py`
- [X] T014 [US3] Implement safe transcript validation, UTF-8 preview loading, and download result adaptation in `whispertube/gui.py`

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T015 [P] Update `README.md` with v0.4 installation, launch, privacy, and local-use instructions
- [X] T016 Run focused GUI tests, the full deterministic suite, `compileall`, and `git diff --check`
- [X] T017 Run the real local browser GUI smoke with the approved public video and small model; inspect transcript/audio artifacts and record any Human Gate
- [ ] T018 Run `$speckit-converge`, update `docs/STATUS.md`, commit, push, and verify deterministic CI

## Dependencies & Execution Order

- T001–T004 precede user-story implementation.
- T005 precedes T006; T007 precedes T008.
- T009 precedes T010; T011 precedes T012.
- T013 precedes T014.
- T015 may run after the interface contract stabilizes; T016–T018 run after all stories.
- Every test task must be executed and observed RED before its implementation task begins.

## Parallel Opportunities

- T015 documentation can run independently after T012 and T014 stabilize behavior.
- Deterministic fixture preparation for T009 and T013 touches the same test file and remains sequential.
- Production tasks intentionally remain sequential because they share `whispertube/gui.py`.

## Implementation Strategy

Deliver P1 first as a testable one-action wrapper, add safe terminal states in P2, then expose only validated
Markdown in P3. Preserve the pipeline as the sole orchestration boundary throughout.
