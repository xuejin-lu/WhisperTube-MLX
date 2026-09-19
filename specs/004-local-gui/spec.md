# Feature Specification: Local Graphical UI

**Feature Branch**: `004-local-gui`

**Created**: 2026-09-19

**Status**: Implemented — review pending

**Input**: Add the first local graphical interface for non-technical use while reusing the approved v0.3 pipeline.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Transcribe One Video Without Terminal (Priority: P1)

A non-technical user opens a local interface, pastes one YouTube video URL, starts transcription,
and receives a completed local transcript without running pipeline commands manually.

**Why this priority**: This is the minimum graphical product journey and the milestone's core value.

**Independent Test**: Inject a fake approved pipeline, submit one URL through the UI handler, and
verify exactly one pipeline request is made and a successful result is returned.

**Acceptance Scenarios**:

1. **Given** the local interface is open and no run is active, **When** the user enters one non-empty
   YouTube URL and selects Transcribe, **Then** one run starts using the approved pipeline boundary.
2. **Given** the URL field is empty or whitespace, **When** the user selects Transcribe, **Then** a
   clear input error is shown and the pipeline is not called.
3. **Given** one run is active, **When** the interface is waiting for completion, **Then** it visibly
   indicates that transcription is running and does not silently start a duplicate run.

---

### User Story 2 - Understand Success and Failure (Priority: P2)

A user can see whether the run is waiting, running, successful, or failed, and receives the approved
cause-specific pipeline error instead of a traceback or generic failure.

**Why this priority**: Local ML work can take minutes and actionable state is essential for trust.

**Independent Test**: Inject successful and failing pipeline functions and verify the returned UI
state, category, message, transcript path, and absence of internal traceback content.

**Acceptance Scenarios**:

1. **Given** the pipeline succeeds, **When** the run completes, **Then** success status names the
   generated transcript and the interface exposes no temporary audio artifact.
2. **Given** the pipeline reports download, dependency, model, inference, output, or cleanup failure,
   **When** the run completes, **Then** the interface preserves that category and actionable message.
3. **Given** an unexpected internal exception, **When** the run completes, **Then** a local application
   error is shown without exposing a traceback, credentials, browser profile, or private file content.

---

### User Story 3 - Preview and Save Markdown (Priority: P3)

After a successful run, a user can read the generated Markdown in the local interface and download
the same Markdown artifact using its safe filename.

**Why this priority**: The transcript becomes useful without requiring the user to locate it in Terminal.

**Independent Test**: Return a local UTF-8 Markdown fixture from a fake pipeline and verify preview
content and downloadable artifact metadata match that fixture byte-for-byte.

**Acceptance Scenarios**:

1. **Given** a successful non-empty UTF-8 Markdown transcript, **When** the result is displayed, **Then**
   the complete Markdown is available for preview and download.
2. **Given** a transcript result is missing, unreadable, outside the approved transcript roots, or not
   Markdown, **When** the UI prepares the result, **Then** it reports an output error and does not expose
   an arbitrary local file for download.
3. **Given** a previous successful result, **When** a new run starts or fails, **Then** stale preview and
   download output are cleared before the new result is shown.

### Edge Cases

- The URL contains playlist parameters; approved single-video normalization remains authoritative.
- A user submits whitespace or repeatedly activates the action while a job is queued/running.
- The pipeline returns a relative transcript path, an allowed absolute path, or a disallowed path.
- The transcript is missing, empty, unreadable, invalid UTF-8, or has a non-Markdown suffix.
- A pipeline error message includes cleanup residual-artifact context from v0.3.
- Browser-cookie fallback requires a login or macOS permission during a real local run.
- The configured local port is unavailable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The product MUST provide a local graphical interface with one URL input and one clearly
  labeled Transcribe action for a single video.
- **FR-002**: The interface MUST call the approved `whispertube.pipeline` orchestration boundary and
  MUST NOT duplicate acquisition, transcription, URL normalization, cleanup, or formatting logic.
- **FR-003**: Empty or whitespace-only input MUST produce a visible input error without calling the pipeline.
- **FR-004**: The interface MUST expose distinct idle, running, success, and error states and MUST avoid
  silently launching duplicate work from one interaction while a run is active. The Transcribe action
  MUST be restored after every terminal success or failure.
- **FR-005**: Successful completion MUST expose the generated transcript filename, complete UTF-8
  Markdown preview, and a download/save action for that same artifact.
- **FR-006**: Preview/download MUST accept only a non-empty `.md` regular file resolved within the
  configured approved transcript output root; arbitrary or pre-existing unrelated files MUST not be exposed.
  Framework-level file serving MUST NOT whitelist the whole transcript directory (or any parent directory)
  when that would make unrelated files directly addressable; only the validated result artifact (or a safe
  framework cache copy of that validated artifact) may become downloadable.
- **FR-007**: Starting a new run or reporting failure MUST clear stale transcript preview and download state.
- **FR-008**: Pipeline failures MUST retain their approved category and actionable message; unexpected
  failures MUST be reported as an application error without a traceback or sensitive local data.
- **FR-009**: The GUI MUST bind only to the local loopback interface, MUST NOT create a public share or
  tunnel, MUST disable direct event-API bypass, and MUST retain strict same-origin safeguards. Framework
  telemetry and monitoring MUST be disabled by default.
- **FR-010**: Media, transcripts, cookies, browser profiles, credentials, and model data MUST remain local;
  the GUI MUST NOT add uploads, hosted processing, accounts, databases, analytics, or paid services.
- **FR-011**: The default quality target MUST remain the approved large-v3 model while launch-time local
  configuration MAY select a compatible smaller model for smoke testing without adding a required user control.
- **FR-012**: Deterministic tests MUST cover UI request/result logic, state clearing, path validation,
  cause-specific errors, and local-only launch configuration without YouTube, model downloads, browser
  credentials, or Apple Silicon hardware.
- **FR-013**: A real local smoke MUST exercise the graphical interface against the approved public video
  with an explicit small MLX model and record loopback-only access, absence of a public share URL,
  transcript retention, temporary-audio cleanup, and any Human Gate.
- **FR-014**: Interactive controls and status/result regions MUST have visible labels, and normal keyboard
  navigation supplied by the local browser interface MUST remain usable.

### Key Entities

- **GUI Request**: One trimmed URL plus launch-time model and approved local output configuration.
- **GUI Result**: Idle/running/success/error state, safe status text, optional Markdown preview, and
  optional approved transcript path.
- **Transcript Artifact**: A non-empty UTF-8 `.md` file inside the configured transcript root, eligible
  for local preview/download but never for GUI cleanup.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can start one-video transcription from the opened local interface with one URL entry
  and one action, without entering a Terminal command after launch.
- **SC-002**: 100% of deterministic state tests distinguish idle, running, success, input error, each
  approved pipeline failure category, and unexpected application failure.
- **SC-003**: 100% of successful deterministic result tests show preview text and downloadable bytes that
  exactly match the generated Markdown artifact.
- **SC-004**: 100% of disallowed, missing, unreadable, empty, non-UTF-8, or non-Markdown result fixtures
  are rejected without exposing an arbitrary local file, including through the framework's direct file-serving
  route rather than only through the GUI callback.
- **SC-005**: Deterministic launch tests prove loopback-only binding, no public share/tunnel, no telemetry,
  and no monitoring endpoint.
- **SC-006**: The full deterministic repository suite completes without live YouTube, browser credentials,
  model downloads, or Apple Silicon hardware.
- **SC-007**: One real local GUI smoke with the approved public video and explicit small model produces a
  non-empty Markdown transcript, leaves no current-run audio, and records any Human Gate truthfully.

## Assumptions

- v0.4 is opened from a local development command; final `.app` packaging belongs to a later milestone.
- One local user and one active transcription job are sufficient for this milestone.
- The UI uses the pipeline's approved output directory and model defaults unless launch-time local
  configuration overrides them for testing.
- Multiple users/jobs, a visible model selector, packaging, summarization, diarization, timestamps,
  playlists, accounts, databases, and hosted deployment are deferred beyond v0.4.
- Browser rendering of Markdown is a preview; downloaded bytes remain the authoritative artifact.
- Anonymous acquisition is expected for the approved smoke video; browser login or macOS permission is
  a Human Gate only if the local fallback actually requests it.
