# Feature Specification: End-to-End CLI Pipeline

**Feature Branch**: `003-end-to-end-cli`

**Created**: 2026-09-19

**Status**: In Progress

**Input**: Compose the approved local YouTube audio acquisition and MLX Whisper transcription stages into one privacy-preserving command-line pipeline.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Produce a Transcript from One YouTube URL (Priority: P1)

A maintainer runs one command with one YouTube video URL and receives one Taiwan Traditional Chinese Markdown transcript without manually running the download and transcription stages separately.

**Why this priority**: This is the first complete product path and delivers the milestone's core value.

**Independent Test**: Inject fake acquisition and transcription boundaries, invoke the pipeline with a valid URL, and verify each stage receives the expected local path/configuration and returns one transcript path.

**Acceptance Scenarios**:

1. **Given** a valid single-video URL and available local stages, **When** the user invokes the pipeline, **Then** it downloads one local audio artifact, transcribes it with the selected Chinese model configuration, and prints one Markdown transcript path.
2. **Given** a URL with playlist parameters, **When** the user invokes the pipeline, **Then** only the current video is processed and one transcript path is produced.
3. **Given** an explicit compatible model and allowed transcript output directory, **When** the user invokes the pipeline, **Then** those selections are passed unchanged to transcription.

---

### User Story 2 - Handle Temporary Audio Safely (Priority: P2)

A maintainer can rely on the pipeline to clean downloaded temporary audio after a run, while keeping the generated transcript and any pre-existing local files intact.

**Why this priority**: Downloaded media is private runtime data and must not accumulate or be committed.

**Independent Test**: Use a fake acquisition boundary that creates a temporary audio file and a fake transcription boundary, then verify the pipeline removes only the file it acquired after success and after a transcription failure.

**Acceptance Scenarios**:

1. **Given** the pipeline acquired an audio artifact during this run, **When** transcription succeeds, **Then** the acquired audio is removed and the Markdown transcript remains.
2. **Given** the pipeline acquired an audio artifact during this run, **When** transcription fails, **Then** the acquired audio is still removed and the original failure is reported.
3. **Given** acquisition fails before reporting an artifact, **When** the pipeline exits, **Then** it does not delete any pre-existing media or transcript path.

---

### User Story 3 - Diagnose the Failing Stage (Priority: P3)

A maintainer receives an actionable non-zero error that identifies whether failure came from download, transcription dependency/model/inference, or transcript output handling.

**Why this priority**: A composed CLI must preserve the actionable boundaries proven in v0.1 and v0.2.

**Independent Test**: Inject failures from each stage and verify their category, message, non-zero exit, and cleanup behavior without network access, model downloads, or Apple Silicon hardware.

**Acceptance Scenarios**:

1. **Given** acquisition rejects or cannot download a URL, **When** the pipeline runs, **Then** the command exits non-zero with a download-specific error and does not call transcription.
2. **Given** transcription reports a dependency, model, inference, or output failure, **When** the pipeline runs, **Then** the command preserves that cause-specific error category and exits non-zero.

### Edge Cases

- The acquisition stage returns a path outside the configured temporary audio directory.
- A transcript output path already exists and the transcription stage refuses to overwrite it.
- Temporary audio has already disappeared by the time cleanup is attempted.
- Cleanup itself fails after a successful transcription.
- A local browser-cookie fallback needs macOS permission or login during a real smoke run.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide one CLI command and reusable function that accept one YouTube URL and compose the existing local acquisition and transcription stages without duplicating either stage's validation or implementation logic.
- **FR-002**: The pipeline MUST process only one current YouTube video and preserve approved URL normalization behavior when playlist parameters are present.
- **FR-003**: The pipeline MUST allow an allowed transcript output directory and explicit compatible transcription model; omitted options MUST retain approved v0.2 defaults.
- **FR-004**: Audio acquired by the pipeline MUST be placed in an ignored temporary local directory and MUST be removed after transcription succeeds or fails. It MUST remove only audio acquired during the current run.
- **FR-005**: The pipeline MUST leave the generated Markdown transcript intact after successful cleanup and MUST NOT delete pre-existing media, transcripts, cookies, model caches, or credentials.
- **FR-006**: The pipeline MUST preserve a download failure as distinct from a transcription dependency, model, inference, or output failure, with an actionable non-zero CLI result.
- **FR-007**: If cleanup fails after a successful transcript is written, the pipeline MUST report an actionable cleanup failure without deleting the transcript or misreporting the transcription result.
- **FR-008**: The pipeline MUST keep media and private data local and MUST NOT add hosted processing, telemetry, playlists, batch operation, summarization, diarization, timestamps, or a GUI.
- **FR-009**: The system MUST provide deterministic injected-stage tests for composition, propagated options, cleanup, and cause-specific failures; CI MUST not need YouTube, browser cookies, model downloads, or Apple Silicon hardware.

### Key Entities

- **Pipeline Run**: One URL, optional model/output selections, acquired temporary audio path, transcript result, and final success or stage-specific failure.
- **Temporary Audio Artifact**: A local audio file created by this pipeline run and eligible for cleanup only after acquisition reports its path.
- **Transcript Artifact**: Existing UTF-8 Taiwan Traditional Chinese Markdown output owned by transcription and never eligible for pipeline cleanup.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For an available public single-video URL and compatible local model, one command writes exactly one non-empty Markdown transcript and reports its path without a separate manual stage.
- **SC-002**: 100% of deterministic orchestration tests verify that audio created by the current run is removed after both success and transcription failure, while the transcript is retained after success.
- **SC-003**: 100% of deterministic stage-failure tests report a non-zero result whose category distinguishes download from dependency/model/inference/output/cleanup failure.
- **SC-004**: Deterministic CI completes without network media acquisition, browser credentials, model downloads, or Apple Silicon hardware.
- **SC-005**: A local smoke run records selected model, transcript path, temporary-audio cleanup outcome, and any human gate without recording private media contents or credentials.

## Assumptions

- Existing v0.1 and v0.2 boundaries are reused rather than reimplemented.
- `temp/pipeline-audio/` is an ignored runtime directory owned by the pipeline for current-run audio.
- Cleanup is attempted after acquisition reports an artifact; a missing artifact is already clean, while other cleanup errors are reported.
- Large-v3 remains the default target and a smaller explicit model is suitable for smoke verification.
- No browser permission/login is expected for the approved public smoke URL; if one appears, it is a human gate and the run stops without credentials.
