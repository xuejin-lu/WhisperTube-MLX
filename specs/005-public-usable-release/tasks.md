---

description: "Task list for the v1.0 public usable release"
---

# Tasks: Public Usable Release

**Input**: Design documents from `/specs/005-public-usable-release/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/release.md`, `quickstart.md`

**Tests**: Required by the project constitution and v1.0 specification. Every behavior-changing task follows RED → GREEN → REFACTOR.

## Phase 1: Setup

**Purpose**: Establish the release artifact surface without changing the approved pipeline.

- [x] T001 Create the release script directory and executable-file placeholders at `scripts/setup_macos.sh` and `scripts/launch_macos.sh`.
- [x] T002 [P] Add the v1.0 metadata file `VERSION` and document the feature-owned release files in `specs/005-public-usable-release/plan.md`.

---

## Phase 2: Foundational Tests and Contracts

**Purpose**: Create the failing deterministic contract tests that block release-path implementation.

**⚠️ CRITICAL**: Tests in this phase must fail for the expected missing-behavior reason before implementation tasks begin.

- [x] T003 [P] Add RED tests for version consistency, `--version`, supported/unsupported host facts, and stable diagnostic codes in `tests/test_release.py`.
- [x] T004 [P] Add RED tests for approved local paths, non-destructive configuration, model defaults, and loopback-only release configuration in `tests/test_release.py`.
- [x] T005 [P] Add RED artifact-safety tests for tracked/release files and machine-specific paths in `tests/test_release_artifacts.py`.

**Checkpoint**: The release-path tests fail only because the v1.0 release module/scripts/docs are not implemented.

---

## Phase 3: User Story 1 - Install and Launch Locally (Priority: P1) 🎯 MVP

**Goal**: A supported Apple Silicon user can diagnose prerequisites, prepare an isolated environment, and launch the local GUI from a clean checkout or source archive.

**Independent Test**: Run the release diagnostics with injected supported and unsupported facts, then execute setup/launch script tests with a temporary fake toolchain and confirm success/failure behavior without network or MLX.

### Implementation for User Story 1

- [x] T006 [US1] Implement version loading, release configuration, host prerequisite checks, stable diagnostic codes, and `python -m whispertube.release --version/--check` in `whispertube/version.py` and `whispertube/release.py`.
- [x] T007 [US1] Make the RED unit tests from `tests/test_release.py` pass for version, host, path, model, and loopback contracts; record GREEN evidence before refactoring.
- [x] T008 [US1] Implement idempotent non-destructive setup and prerequisite failure handling in `scripts/setup_macos.sh`, using only the project `.venv` and tracked requirement files.
- [x] T009 [US1] Implement prepared-environment validation and local GUI delegation in `scripts/launch_macos.sh`, preserving caller arguments and rejecting missing setup.
- [x] T010 [US1] Add script-level deterministic tests or safe shell fakes in `tests/test_release.py` for setup reruns, missing `ffmpeg`, missing `.venv`, paths with spaces, and absence of `--share`/non-loopback launch options.
- [x] T011 [US1] Refactor release diagnostics and shell quoting only after focused release tests remain green.

**Checkpoint**: User Story 1 is independently usable and testable without a model download.

---

## Phase 4: User Story 2 - Use the Public Release Workflow (Priority: P1)

**Goal**: Public setup/launch documentation exposes the approved v0.4 GUI and v0.3 pipeline without weakening local privacy, cleanup, model, or error contracts.

**Independent Test**: Run the existing deterministic GUI/pipeline suite plus new release configuration tests, then use the launch path with the explicit small model during local Apple Silicon smoke.

### Tests for User Story 2

- [x] T012 [P] [US2] Add RED tests asserting the documented default model, explicit smoke-model example, output roots, and loopback/privacy settings in `tests/test_release.py`.
- [x] T013 [P] [US2] Review existing deterministic GUI regression assertions in `tests/test_gui.py` against the v1.0 launch/configuration contract; no v0.4 boundary change was required.

### Implementation for User Story 2

- [x] T014 [US2] Update `README.md` with clean-release setup, launch, default/smoke model, first-use cache, local artifact, cleanup, and troubleshooting instructions without changing the approved workflow semantics.
- [x] T015 [US2] Add v1.0 release-path examples and privacy/cleanup boundaries to `specs/005-public-usable-release/quickstart.md` and keep them consistent with `README.md`.
- [x] T016 [US2] Make the User Story 2 RED tests pass and run the focused GUI/pipeline/release tests to confirm no public share, telemetry, broad file serving, or cleanup regression.

**Checkpoint**: User Story 2 remains independently testable using the existing pipeline/GUI and the v1.0 release instructions.

---

## Phase 5: User Story 3 - Diagnose, Clean Up, and Prepare a Release (Priority: P2)

**Goal**: Users and maintainers can diagnose common failures, clean up safely, and prepare a reviewable candidate without publishing it.

**Independent Test**: Read the troubleshooting/release docs against each required failure category, run artifact-safety tests, and verify the release checklist contains evidence and an explicit no-publication boundary.

### Tests for User Story 3

- [x] T017 [P] [US3] Add RED tests for troubleshooting category coverage, version/release-plan consistency, and no-publication wording in `tests/test_release_artifacts.py`.
- [x] T018 [P] [US3] Add RED tests for safe cleanup guidance that distinguishes `.venv`/runtime roots from transcripts, cookies, credentials, and model caches in `tests/test_release_artifacts.py`.

### Implementation for User Story 3

- [x] T019 [P] [US3] Add actionable prerequisite, dependency, model-cache, yt-dlp, browser-cookie, Keychain/macOS-permission, decoder, output-path, and permission guidance in `docs/TROUBLESHOOTING.md`.
- [x] T020 [P] [US3] Add versioned tag/release-notes/evidence/artifact-inspection/withdrawal checklist and explicit final-approval boundary in `docs/RELEASE.md`.
- [x] T021 [US3] Implement the artifact-safety scan exercised by `tests/test_release_artifacts.py` without reading or exporting private runtime data.
- [x] T022 [US3] Make the User Story 3 RED tests pass, then refactor documentation and diagnostics while the focused suite stays green.

**Checkpoint**: User Story 3 is independently reviewable and does not publish a GitHub Release.

---

## Phase 6: Polish and Cross-Cutting Validation

**Purpose**: Verify the candidate against the spec, preserve status evidence, and prepare the coherent review handoff.

- [x] T023 [P] Update `docs/STATUS.md` with v1.0 implementation state, verified deterministic facts, smoke/CI evidence, unresolved risks, and exact review state.
- [x] T024 [P] Run artifact inspection over tracked files and candidate source contents; remove only newly introduced release-scope runtime/private artifacts if any are found, never existing user work.
- [x] T025 Run the full deterministic suite with `python -m unittest discover -s tests -v`, whitespace checks, and any available local lint/static checks; record results in `docs/STATUS.md`.
- [x] T026 Run the local Apple Silicon setup/launch and approved public-video `mlx-community/whisper-tiny` smoke when technically available; verify Markdown output, cleanup, loopback-only behavior, and no public share URL.
- [x] T027 Run `$speckit-converge` for `specs/005-public-usable-release/`, append any genuinely remaining tasks to `tasks.md`, and repeat implementation if convergence adds work; convergence found no remaining tasks.
- [x] T028 Commit the coherent v1.0 implementation and documentation changes, push the current branch, and record the commit/CI state in `docs/STATUS.md` without publishing a GitHub Release.

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 has no dependency and creates the release surface.
- Phase 2 depends on Phase 1 and blocks release implementation until RED failures are observed.
- User Story 1 depends on Phase 2 and is the MVP release path.
- User Story 2 depends on the User Story 1 launch contract and preserves the existing v0.4/v0.3 behavior.
- User Story 3 depends on the release configuration from User Story 1 and the documented workflow from User Story 2.
- Phase 6 depends on all desired stories and any converge-created tasks.

### User Story Dependencies

- **US1**: No story dependency after foundational tests.
- **US2**: Depends on US1's launch/configuration contract and existing approved v0.4/v0.3 code.
- **US3**: Depends on US1 version/configuration and US2 documentation boundaries.

### Parallel Opportunities

- T003–T005 can run in parallel because they add tests in separate concerns before implementation.
- T019 and T020 can run in parallel because they edit separate documentation files.
- T023 and T024 can run in parallel after implementation stabilizes.

## Implementation Strategy

1. Establish tests and the pure release configuration first.
2. Deliver US1 as the smallest usable MVP: diagnose, setup, launch.
3. Add US2 documentation and regression coverage without changing pipeline semantics.
4. Add US3 troubleshooting, artifact inspection, and release planning.
5. Run local smoke, full tests, converge, update status, commit, push, and leave actual GitHub Release publication for explicit review approval.

---

## Phase 7: Convergence — clean-path release remediation

**Purpose**: Close the repository-review blocker where a clean user machine has no global `yt-dlp`.

- [x] T029 [US1] Add RED deterministic shell/runtime tests in `tests/test_release.py` using a temporary minimal project environment and PATH without global `yt-dlp`; prove that `scripts/launch_macos.sh` preserves arguments and makes the project-owned `.venv/bin/yt-dlp` discoverable to the launched process per FR-002, US1 AC3, and SC-001 (missing).
- [x] T030 [US1] Add RED execution tests for setup rerun safety, missing native prerequisite, missing `.venv`, paths containing spaces, and launcher argument preservation in `tests/test_release.py`; replace source-text-only assertions for T010 with fake-toolchain behavior coverage (T010, partial).
- [x] T031 [US1] Implement the smallest safe clean-path fix in `scripts/launch_macos.sh` by explicitly prepending the project `.venv/bin` to `PATH` before launching `whispertube.gui`, without changing loopback or public-sharing boundaries (FR-002, `contracts/release.md`, partial).
- [x] T032 [P] Update `docs/RELEASE.md` and `docs/STATUS.md` with clean-PATH test evidence, exact remediation commit/CI state, and the still-separate GitHub Release publication approval (SC-001, T010, partial).
- [x] T033 Run focused release tests, the full deterministic suite, clean-PATH launcher verification, real Apple Silicon small-model smoke, artifact inspection, exact-SHA CI, and a follow-up `$speckit-converge`; repeat implementation if any remaining task is found (SC-001, SC-003, SC-004, partial).
