---

description: "Task list for local YouTube audio acquisition"
---

# Tasks: Local YouTube Audio Acquisition

**Input**: Design documents from `/specs/001-local-youtube-audio/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli.md, quickstart.md

**Tests**: Deterministic tests are required by the feature specification and project constitution.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish Spec Kit artifacts and the existing small Python package layout.

- [X] T001 Initialize Spec Kit v1.0.3 artifacts under `.specify/` and `.agents/skills/`
- [X] T002 Create the v0.1 feature specification and requirements checklist in `specs/001-local-youtube-audio/spec.md` and `specs/001-local-youtube-audio/checklists/requirements.md`
- [X] T003 Create the implementation plan, research notes, data model, CLI contract, quickstart, and feature pointer under `specs/001-local-youtube-audio/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Reconcile the pre-Spec-Kit implementation with deterministic test and privacy gates.

- [X] T004 Establish the existing standard-library test entry point in `tests/test_youtube.py`
- [ ] T005 Add mocked CLI subprocess tests for missing downloader, non-zero acquisition exit, and unwritable output-directory behavior in `tests/test_youtube.py`
- [ ] T006 Add a test that invalid URLs fail before `subprocess.run` is invoked in `tests/test_youtube.py`

**Checkpoint**: Deterministic validation covers both pure parsing and CLI failure boundaries.

---

## Phase 3: User Story 1 - Download One Video's Audio (Priority: P1) 🎯 MVP

**Goal**: Normalize one supported URL and construct or run a single-video local audio acquisition.

**Independent Test**: Run the deterministic suite, inspect the printed command for a playlist-bearing
URL, then run the anonymous smoke command against the public test video and inspect `temp/audio/`.

### Tests for User Story 1

- [X] T007 [P] [US1] Cover watch, `youtu.be`, Shorts, and playlist-bearing URLs in `tests/test_youtube.py`
- [ ] T008 [US1] Add a CLI contract test for `--print-command` and canonical single-video output in `tests/test_youtube.py`

### Implementation for User Story 1

- [X] T009 [US1] Implement canonical single-video URL normalization in `whispertube/youtube.py`
- [X] T010 [US1] Implement `yt-dlp` argv construction with `--no-playlist`, best-audio selection, and ignored output template in `whispertube/youtube.py`
- [X] T011 [US1] Implement local output-directory creation and downloader invocation in `whispertube/youtube.py`

**Checkpoint**: User Story 1 is code-complete; live acquisition remains pending local smoke evidence.

---

## Phase 4: User Story 2 - Recover from YouTube Access Checks (Priority: P2)

**Goal**: Support an explicit local browser-session retry without exporting credential files.

**Independent Test**: Inspect the constructed fallback argv for the browser option and verify no
cookie-file option is accepted or generated; run the fallback only if anonymous smoke access is blocked.

### Tests for User Story 2

- [X] T012 [P] [US2] Cover browser-session argument construction in `tests/test_youtube.py`
- [ ] T013 [US2] Add a privacy contract assertion that browser fallback argv contains no cookie-file export option in `tests/test_youtube.py`

### Implementation for User Story 2

- [X] T014 [US2] Add the explicit `--cookies-from-browser` fallback option to `whispertube/youtube.py`
- [ ] T015 [US2] Record anonymous and browser-session smoke outcomes, including any human authorization gate, in `docs/STATUS.md`

**Checkpoint**: User Stories 1 and 2 are independently testable without committing credentials.

---

## Phase 5: User Story 3 - Reject Invalid Requests Clearly (Priority: P3)

**Goal**: Reject invalid input before a downloader process starts and return actionable errors.

**Independent Test**: Run invalid URL fixtures and mocked missing-downloader/failure cases in the
deterministic suite; confirm no live network request is needed.

### Tests for User Story 3

- [X] T016 [P] [US3] Cover unsupported hosts and invalid video IDs in `tests/test_youtube.py`
- [ ] T017 [US3] Cover empty, malformed, and missing-video-ID CLI errors in `tests/test_youtube.py`

### Implementation for User Story 3

- [X] T018 [US3] Implement validation errors for unsupported URL forms in `whispertube/youtube.py`
- [ ] T019 [US3] Implement actionable missing-executable handling, unwritable output-directory handling, and downloader exit-code propagation in `whispertube/youtube.py`

**Checkpoint**: All three user stories have deterministic acceptance coverage; live-service evidence is tracked separately.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Converge documentation, validation evidence, and repository quality gates.

- [ ] T020 [P] Update `README.md` and `specs/001-local-youtube-audio/quickstart.md` with verified local smoke results
- [ ] T021 Run the full deterministic suite and quickstart validation, then record verified facts in `docs/STATUS.md`
- [ ] T022 Run `git diff --check` and inspect ignored runtime paths for credentials or downloaded media before commit in the repository root
- [ ] T023 Push the completed migration and verification commit, then check `.github/workflows/test.yml` CI status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1**: Complete; no dependencies.
- **Phase 2**: Depends on Phase 1 and blocks new behavior work.
- **Phase 3 (US1)**: Depends on Phase 2; MVP scope.
- **Phase 4 (US2)**: Depends on the US1 command contract but is independently testable.
- **Phase 5 (US3)**: Depends on the shared CLI boundary from Phase 2 and can proceed after it.
- **Phase 6**: Depends on all desired implementation and verification tasks.

### User Story Dependencies

- **US1 (P1)**: No story dependency after Phase 2.
- **US2 (P2)**: Uses the US1 downloader command but adds only an optional browser-session argument.
- **US3 (P3)**: Uses the shared URL/CLI validation boundary; it does not require browser access.

### Parallel Opportunities

- T005 and T006 can be implemented in parallel only if they are coordinated before editing the same
  test file; otherwise execute them sequentially.
- T007 and T012 can be reviewed independently as existing tests cover different acceptance paths.
- T016 can run independently of browser-session work.
- T020 and T022 touch different files and can be prepared in parallel after implementation.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete the foundational test gaps in Phase 2.
2. Validate the existing US1 implementation with deterministic tests.
3. Run the anonymous local smoke test against the public test video.
4. Stop and record evidence before selecting the v0.2 transcription dependency.

### Incremental Delivery

1. Complete Phase 2 and US1 to establish one-video audio acquisition.
2. Complete US2 only if anonymous access needs the browser-session fallback.
3. Complete US3 error coverage and the cross-cutting validation/reporting tasks.
4. Run convergence before declaring v0.1 complete.
