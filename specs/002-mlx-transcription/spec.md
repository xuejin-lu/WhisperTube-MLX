# Feature Specification: Local MLX Transcription

**Feature Branch**: `002-mlx-transcription`

**Created**: 2026-09-16

**Status**: In Progress

**Input**: User description: "Establish a local Apple Silicon MLX-compatible Whisper transcription path for Chinese audio transcripts with local-only processing, model and dependency error handling, and no cloud transcription dependency."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Transcribe Local Audio to Chinese Markdown (Priority: P1)

As a maintainer, I want to provide a local audio file and receive a Chinese Markdown transcript
so that downloaded audio can be converted into readable text without leaving the Mac.

**Why this priority**: Local transcription is the core v0.2 value and the next independently
verifiable stage after v0.1 audio acquisition.

**Independent Test**: Give the transcription command a local fixture audio file and a locally
available MLX Whisper model; verify that one non-empty UTF-8 Markdown transcript is created and
contains Chinese text without an upload or hosted transcription request.

**Acceptance Scenarios**:

1. **Given** a readable local audio file and an available MLX-compatible Whisper model, **When**
   the maintainer starts transcription in Chinese mode, **Then** exactly one Markdown transcript
   is written beneath the configured ignored local output directory, is non-empty, and contains
   readable transcript paragraphs.
2. **Given** a local audio file containing Chinese speech, **When** transcription completes, **Then**
   the transcript contains recognizable Taiwan Traditional Chinese text and uses UTF-8 encoding.
3. **Given** a source audio file outside the repository, **When** transcription completes, **Then**
   the source remains unchanged and no audio or transcript is uploaded to a hosted service.

---

### User Story 2 - Use Apple Silicon MLX Locally (Priority: P2)

As a maintainer, I want the transcription path to use an MLX-compatible Whisper implementation on
Apple Silicon so that the workload runs locally with the target hardware acceleration path.

**Why this priority**: The product is explicitly local-first and Apple-Silicon-first; a generic
hosted or CPU-only path would not satisfy the v0.2 milestone.

**Independent Test**: On an Apple Silicon Mac with the selected dependency and a small local model,
run a short fixture and record successful MLX-backed transcription without requiring a cloud API.

**Acceptance Scenarios**:

1. **Given** an Apple Silicon Mac and a supported local model, **When** the maintainer runs the
   documented smoke command, **Then** the model loads through the MLX Whisper path and returns a
   transcript without hosted inference.
2. **Given** the preferred large-v3 model is too large for a constrained local run, **When** the
   maintainer selects a smaller supported model explicitly, **Then** the same local contract works
   while the default quality target remains documented.

---

### User Story 3 - Report Transcription Failures Clearly (Priority: P3)

As a maintainer, I want missing inputs, dependencies, models, and unusable output locations to fail
with actionable messages so that a local pipeline failure can be corrected without guessing.

**Why this priority**: Clear boundaries prevent a later downloader-to-transcriber integration from
reporting a misleading success or hiding the actual local prerequisite.

**Independent Test**: Supply each invalid or unavailable prerequisite independently and verify a
non-zero result, a cause-specific message, and no success transcript being reported.

**Acceptance Scenarios**:

1. **Given** a missing, unreadable, or unsupported audio input, **When** transcription starts,
   **Then** it exits non-zero with an actionable input error before model inference.
2. **Given** the MLX Whisper dependency or requested model is unavailable, **When** transcription
   starts, **Then** it exits non-zero with an actionable dependency/model error and does not create
   a misleading transcript.
3. **Given** the output directory cannot be created or written, **When** transcription starts,
   **Then** it exits non-zero with an actionable output error before model inference.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- The input path does not exist, is a directory, is unreadable, or has an unsupported audio format.
- The output directory is absent, outside the documented ignored runtime paths, or unwritable.
- The MLX Whisper package is not installed, the model cannot be resolved, or the model is too large
  for the available local memory.
- The recognizer returns no text or text that cannot be encoded as UTF-8.
- The same output path already contains a transcript; the command must not silently overwrite it.
- A local model cache or downloaded model artifact must remain outside versioned source paths.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: The system MUST accept one readable local audio file and produce one UTF-8 Markdown
  transcript in a configured ignored local output directory.
- **FR-002**: The system MUST run speech recognition locally through an MLX-compatible Whisper
  implementation on the target Apple Silicon Mac and MUST NOT require a hosted transcription API.
- **FR-003**: The system MUST support Chinese transcription mode and MUST pass an explicit
  transcription task rather than silently translating speech into English.
- **FR-004**: The default model configuration MUST target the MLX Community Whisper large-v3 model;
  an explicitly selected smaller compatible model MUST be supported for constrained smoke runs.
- **FR-005**: The system MUST write a Markdown document containing Taiwan Traditional Chinese
  transcript text grouped into readable paragraphs targeting roughly 500 Chinese characters per
  paragraph, plus a minimal source/model metadata header, without embedding audio bytes or
  credentials.
- **FR-006**: The system MUST reject missing, non-file, unreadable, and unsupported input paths
  before model inference with a cause-specific non-zero result.
- **FR-007**: The system MUST report missing MLX Whisper dependency, unavailable model, model-load,
  and inference failures as distinct actionable non-zero errors.
- **FR-008**: The system MUST reject repository-relative output paths outside documented ignored
  runtime directories, may use an explicitly provided local system-temporary path, reject unwritable
  destinations, and MUST NOT overwrite an existing transcript by default.
- **FR-009**: The system MUST keep audio, model caches, and generated transcripts local; it MUST
  NOT upload audio, transcripts, credentials, or telemetry during transcription.
- **FR-010**: The system MUST expose deterministic tests for input validation, model/backend
  selection, output formatting, privacy boundaries, and cause-specific error handling without
  requiring MLX hardware or a live model download.

### Key Entities *(include if feature involves data)*

- **Local Audio Input**: One user-selected audio file path, its readable-file state, and its source
  format as accepted by the local decoder.
- **Whisper Model Source**: A default large-v3 MLX model reference or an explicitly selected local/
  compatible smaller model reference.
- **Transcript Artifact**: One UTF-8 Markdown file containing source metadata and non-empty Chinese
  transcript text under an ignored local output directory.
- **Transcription Run**: The local association of one input, one model source, one language/task
  configuration, and one result or cause-specific failure.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: For a valid local fixture and an available compatible model, one command produces
  exactly one non-empty UTF-8 Markdown transcript and exits successfully.
- **SC-002**: A short Chinese speech fixture produces at least one recognizable Chinese phrase in
  the transcript during local Apple Silicon smoke verification.
- **SC-003**: 100% of deterministic tests for invalid input, missing dependency/model, inference
  failure, output failure, and output collision return non-zero with the specified cause category.
- **SC-004**: Deterministic CI completes without Apple Silicon hardware, model downloads, network
  access, hosted transcription, browser credentials, or private media.
- **SC-005**: Local smoke verification records the selected model, elapsed result, output path, and
  whether any human gate occurred without recording audio contents or credentials.

## Assumptions

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right assumptions based on reasonable defaults
  chosen when the feature description did not specify certain details.
-->

- The target machine is macOS on Apple Silicon and can install the free/open MLX Whisper dependency
  and ffmpeg locally.
- A model may be downloaded from the documented model registry during setup, but inference receives
  local audio and runs locally; model caches are ignored runtime artifacts.
- The default large-v3 model is a quality target, not a CI dependency; a smaller explicit model is
  acceptable for a short smoke run when memory or time is constrained.
- v0.2 produces a plain Markdown transcript only; YouTube orchestration, summarization, diarization,
  translation, word-level timestamps, GUI, and hosted APIs are out of scope.
- The recognizer's returned text is preserved as transcript content; no claims about word-error-rate
  improvement are made without a labeled evaluation corpus.
