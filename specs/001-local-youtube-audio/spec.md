# Feature Specification: Local YouTube Audio Acquisition

**Feature Branch**: `001-local-youtube-audio`

**Created**: 2026-09-16

**Status**: In Progress

**Input**: User description: "Reliably acquire audio from one YouTube video locally on an Apple Silicon Mac, including a local browser-cookie fallback when anonymous access is blocked."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Download One Video's Audio (Priority: P1)

As a maintainer, I want to provide one YouTube video URL and receive a local audio file so that
the file can be used by later transcription stages without sending media to a hosted service.

**Why this priority**: Local audio acquisition is the first product milestone and the prerequisite
for every later transcription workflow.

**Independent Test**: Provide a public test-video URL in a local environment with the required
downloader available, then verify that exactly the requested video is selected and an audio artifact
is created in the designated ignored local directory.

**Acceptance Scenarios**:

1. **Given** a valid YouTube watch URL, **When** the user starts acquisition, **Then** the current
   video is selected and its best available audio is written to the designated local directory.
2. **Given** a valid `youtu.be` or Shorts URL, **When** the user starts acquisition, **Then** it is
   treated as the same single-video request as its canonical watch URL.
3. **Given** a watch URL containing playlist parameters, **When** the user starts acquisition,
   **Then** only the video identified by the video parameter is selected and no playlist batch is
   started.

---

### User Story 2 - Recover from YouTube Access Checks (Priority: P2)

As a maintainer, I want to retry acquisition using my local browser session when anonymous access
is blocked so that I can complete the download without exporting credentials or uploading them.

**Why this priority**: YouTube access checks can prevent the primary flow, while a local browser
session is the privacy-preserving fallback defined for this milestone.

**Independent Test**: In a local environment where anonymous access is unavailable, invoke the
documented browser-session fallback and verify that the request uses local session data only; no
cookie export or repository file is created.

**Acceptance Scenarios**:

1. **Given** anonymous acquisition reports an authentication or anti-bot requirement, **When** the
   user retries with a supported local browser session, **Then** the acquisition request includes
   that session source and does not require a cookie file in the repository.
2. **Given** the browser session cannot be read or is not authorized, **When** the fallback runs,
   **Then** the user receives an actionable error and no credential material is persisted.

---

### User Story 3 - Reject Invalid Requests Clearly (Priority: P3)

As a maintainer, I want invalid or unsupported URLs to fail before any download starts so that
mistakes are clear and do not create misleading output.

**Why this priority**: Early validation prevents unnecessary network work and makes the local tool
safe to use from scripts and later UI layers.

**Independent Test**: Supply empty, malformed, non-YouTube, and video-ID-less URLs and verify that
each is rejected with a clear validation error and no downloader process is started.

**Acceptance Scenarios**:

1. **Given** an empty, malformed, or non-YouTube URL, **When** the user starts acquisition, **Then**
   the request is rejected with a clear validation error before download.
2. **Given** a URL that does not identify one valid video, **When** the user starts acquisition,
   **Then** the request is rejected and no local audio artifact is reported as successful.

### Edge Cases

- A URL may use `http` or `https`, include a timestamp, or include playlist and tracking
  parameters; only the video identity is used for a single-video request.
- A URL with an invalid or missing 11-character video ID must be rejected before invoking the
  downloader.
- The output directory may not exist; acquisition creates it only under the configured local
  runtime path.
- The output directory may exist but be unavailable or unwritable; acquisition fails before the
  downloader starts and reports an actionable output error.
- The downloader executable may be missing or return a non-zero exit status; the user receives an
  actionable error identifying the acquisition failure.
- Browser-session access may require an operating-system permission or interactive login; the
  workflow reports that human gate without copying credentials into the project.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST accept a single valid YouTube watch URL, `youtu.be` URL, or Shorts
  URL and identify exactly one video.
- **FR-002**: The system MUST normalize equivalent supported URL forms to one canonical single-video
  request and MUST ignore playlist parameters for v0.1 acquisition.
- **FR-003**: The system MUST acquire the highest-quality audio-only representation available for
  the requested video into a configured local temporary or runtime directory, preserving its source
  container in v0.1 without requiring format conversion.
- **FR-004**: The system MUST reject empty, malformed, unsupported, or video-ID-less URLs before
  starting acquisition and MUST provide an actionable validation error.
- **FR-005**: The system MUST provide a documented fallback that reads a supported local browser
  session when anonymous acquisition is blocked.
- **FR-006**: The system MUST NOT upload media, browser session data, credentials, or transcripts,
  and MUST NOT write cookie exports or private runtime artifacts into versioned repository paths.
- **FR-007**: The system MUST expose deterministic tests for URL handling and acquisition request
  construction without requiring a live YouTube request.
- **FR-008**: The system MUST return a non-success result when the downloader is unavailable or
  acquisition fails, and the result MUST identify the failure as an acquisition error.
- **FR-009**: The system MUST return a non-success result with an actionable output error when the
  configured runtime directory cannot be created or written, and MUST NOT start the downloader in
  that case.

### Key Entities

- **Video Request**: The user's original URL and its normalized single-video identity, without
  playlist batch semantics.
- **Local Audio Artifact**: The temporary audio file created for the requested video under an
  ignored local runtime directory.
- **Browser Session Source**: An optional local browser session used for authentication fallback;
  it is a credential source, not a repository artifact.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of deterministic URL fixtures covering watch, `youtu.be`, Shorts, playlist-
  bearing watch URLs, and invalid hosts produce the specified accept or reject result.
- **SC-002**: For a reachable public test video, one acquisition attempt produces one audio artifact
  in the configured ignored local directory and does not start playlist batch processing.
- **SC-003**: When anonymous access is blocked but the local browser session is available, the
  fallback completes acquisition without creating a cookie export or other credential file in the
  repository.
- **SC-004**: Missing downloader, invalid input, failed acquisition, and unavailable output
  directory each produce a non-success result with a message that identifies the actionable cause.
- **SC-005**: The deterministic test suite passes in CI without network access, browser credentials,
  private media, or Apple Silicon-specific acceleration.

## Assumptions

- The initial user is the maintainer running the tool on macOS with Apple Silicon and a local
  Python environment.
- The maintainer installs the free local downloader separately when it is not already available.
- The test video is public and may be unavailable or protected by YouTube at any given time; live
  acquisition is therefore a local smoke check rather than a CI dependency.
- The initial milestone needs one audio artifact only; transcription, translation, paragraph
  formatting, and graphical UI remain later milestones.
- Local browser fallback support depends on the browser and operating-system permissions available
  on the maintainer's Mac.
