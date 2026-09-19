# Feature Specification: Public Usable Release

**Feature Branch**: `005-public-usable-release`

**Created**: 2026-09-19

**Status**: Complete — release candidate approved for publication

**Input**: Turn the approved v0.1-v0.4 local pipeline and GUI into a reproducible public release for Apple Silicon macOS users.

## Release Decision

v1.0 ships as a versioned source release with repository-provided setup and launch commands. It does not ship a signed/notarized `.app`, installer package, or background service in this milestone. This is the smallest distribution path that preserves local execution, keeps the Python/MLX environment inspectable and reproducible, and does not imply that macOS signing or notarization has been solved. A future packaged application can be proposed as a separate feature.

## User Scenarios & Testing

### User Story 1 - Install and Launch Locally (Priority: P1)

As an Apple Silicon Mac user who has obtained the v1.0 source release, I want one documented setup path and one documented launch path so that I can run WhisperTube locally without knowing the repository's internal development history.

**Why this priority**: Without a repeatable setup and launch path, the approved pipeline is not a usable public release.

**Independent Test**: Starting from a clean checkout or release archive on a supported Apple Silicon Mac with no project virtual environment, a user can follow the documented prerequisites and setup commands, launch the local GUI, and reach its loopback URL without editing source files.

**Acceptance Scenarios**:

1. **Given** a supported Apple Silicon Mac with a supported native Python and Homebrew available, **When** the user runs the documented setup path, **Then** an isolated project environment is created and all required Python dependencies are installed from pinned project requirements.
2. **Given** the setup path is complete, **When** the user runs the documented launch path, **Then** the GUI binds only to the loopback address, does not create a public share, and opens or reports a local URL.
3. **Given** the user has no globally installed `yt-dlp` executable, but setup installed the pinned project dependency into `.venv`, **When** the launched GUI acquires a YouTube video, **Then** the release path MUST still invoke the project-owned `.venv` yt-dlp successfully without depending on ambient/global PATH state.
4. **Given** a non-Apple-Silicon Mac, unsupported macOS version, non-native Python, or missing required decoder, **When** setup is attempted, **Then** the user receives an actionable prerequisite message and setup does not claim success.
5. **Given** setup has already completed, **When** setup is run again, **Then** it is safe and repeatable without deleting user outputs, model caches, cookies, or unrelated files.

### User Story 2 - Use the Public Release Workflow (Priority: P1)

As a release user, I want the public launch instructions to take me from one YouTube URL to a local Taiwan Traditional Chinese Markdown transcript while retaining the approved privacy and cleanup boundaries.

**Why this priority**: Installation has no user value unless the released workflow still performs the approved end-to-end task.

**Independent Test**: With the release environment prepared, a public test video and an explicit small MLX model can be processed locally, producing a readable Markdown transcript while leaving current-run audio cleaned up and no public endpoint exposed.

**Acceptance Scenarios**:

1. **Given** a completed setup and a valid YouTube URL, **When** the user launches the GUI and submits the URL, **Then** acquisition, local MLX transcription, Taiwan Traditional Chinese conversion, preview, and local Markdown download remain available through the approved v0.4 flow.
2. **Given** the default release configuration, **When** transcription is requested without selecting an alternate model, **Then** the large-v3 quality target remains the default and the user is told that the first model use may download a local model cache.
3. **Given** a user chooses an explicit smaller compatible model for validation, **When** the workflow runs, **Then** it uses that model without changing the documented default.
4. **Given** a successful or failed current run, **When** the run ends, **Then** current-run acquired audio is cleaned according to the approved pipeline rules, the resulting Markdown transcript is retained locally when available, and no media, cookies, transcripts, model cache, or credentials are uploaded or committed.
5. **Given** the local GUI is running, **When** a user inspects its address or attempts a public sharing path, **Then** only loopback access is available and public sharing/tunneling remains disabled.

### User Story 3 - Diagnose, Clean Up, and Prepare a Release (Priority: P2)

As a maintainer or release user, I want version information, safe cleanup guidance, troubleshooting, and a release checklist so that installation failures are actionable and a candidate can be reviewed before any public release is published.

**Why this priority**: A public release must be supportable and reviewable, not merely runnable on the development machine.

**Independent Test**: A deterministic test suite can exercise version/configuration/launcher diagnostics without network or MLX hardware, and a maintainer can follow the documented uninstall and release-review procedure without guessing which local artifacts are safe to remove or publish.

**Acceptance Scenarios**:

1. **Given** an installed checkout or release archive, **When** the user requests version information, **Then** the same v1.0 version is reported by the documented project metadata and release documentation.
2. **Given** a missing prerequisite, failed dependency installation, missing model cache, decoder failure, or YouTube acquisition failure, **When** the user follows troubleshooting guidance, **Then** the relevant failure category, diagnostic command, and safe next action are documented without requesting credentials or uploading private data.
3. **Given** a user wants to remove the local installation, **When** they follow uninstall guidance, **Then** the project environment and documented project-local runtime artifacts can be removed while separately warning that model caches and user transcripts may be outside the project directory and require an explicit user choice.
4. **Given** a release candidate, **When** the maintainer follows the release checklist, **Then** version metadata, deterministic tests, Apple Silicon smoke evidence, CI state, and artifact inspection are recorded before publication; the checklist does not publish a GitHub Release automatically.
5. **Given** repository or release artifacts are inspected, **When** privacy checks are performed, **Then** cookies, credentials, browser profiles, model caches, downloaded media, private transcripts, and machine-specific absolute paths are absent from reviewable artifacts.

### Edge Cases

- Setup is interrupted after creating an environment or installing only part of the dependencies; rerunning setup must recover without broad deletion.
- Python exists but is x86_64 under Rosetta, or the host is Intel; the prerequisite diagnostic must distinguish unsupported architecture from a missing Python executable.
- Homebrew or `ffmpeg` is unavailable; setup must identify the missing decoder and point to the supported installation action without silently installing unrelated software.
- Network access is unavailable during dependency or model acquisition; the user must see which stage failed and what remains local.
- The model cache already exists, is incomplete, or is stored outside the checkout; troubleshooting and uninstall guidance must not assume it is safe to delete.
- A release archive is unpacked into a path containing spaces or non-ASCII characters; setup and launch paths must remain usable or provide an actionable limitation.
- A user sets ambient Gradio file-serving configuration or requests a non-approved output directory; the approved v0.4 privacy boundary must remain enforced.
- A release candidate contains ignored runtime files in the working tree; artifact inspection must detect them before commit or publication.
- An update from a prior checkout is attempted with an existing `.venv`, outputs, or model cache; setup must preserve those local artifacts.

## Requirements

### Functional Requirements

- **FR-001**: The release MUST state that v1.0 targets macOS on native Apple Silicon and MUST provide prerequisite checks for host architecture, supported macOS version, native Python, and the required local decoder.
- **FR-002**: The release MUST provide one setup path that creates or reuses an isolated project environment and installs all pinned Python dependencies required by the GUI and approved local pipeline. Runtime executables installed into that environment (including `yt-dlp`) MUST remain discoverable when the documented launcher runs, without requiring a separate global installation.
- **FR-003**: Setup MUST be repeatable and MUST NOT delete or overwrite user outputs, model caches, cookies, credentials, or unrelated files.
- **FR-004**: The release MUST provide one launch path that starts the approved GUI from the prepared environment and reports its local loopback URL.
- **FR-005**: The release MUST fail with actionable diagnostics when a required prerequisite or dependency is missing, incompatible, or installed for the wrong CPU architecture.
- **FR-006**: The setup and launch paths MUST work from a clean checkout or versioned source archive without requiring repository-specific historical knowledge or source edits.
- **FR-007**: The released workflow MUST preserve the approved single-video local acquisition, local MLX Whisper transcription, OpenCC Taiwan Traditional Chinese conversion, Markdown output, cleanup, and cause-specific error boundaries.
- **FR-008**: The release MUST preserve the large-v3 model as the default quality target and MUST document an explicit smaller-model option for local validation.
- **FR-009**: Model downloads and caches MUST remain local, MUST be described as first-use behavior, and MUST NOT be bundled into the source release or copied into repository-managed artifacts.
- **FR-010**: The GUI MUST continue to bind to loopback only, disable public sharing and telemetry/monitoring, and reject ambient configuration that would broaden approved file serving.
- **FR-011**: The release MUST document safe locations for runtime audio, transcripts, temporary files, and model caches, and MUST state which artifacts are ignored and which are retained after a run.
- **FR-012**: The release MUST document an uninstall/cleanup path that distinguishes disposable project environment/runtime files from user transcripts and model caches requiring explicit user choice.
- **FR-013**: The release MUST expose one consistent v1.0 version value through project metadata and the documented user-facing version command or diagnostic.
- **FR-014**: Troubleshooting documentation MUST cover unsupported architecture/OS, native Python mismatch, missing `ffmpeg`, dependency installation failure, model download/cache failure, yt-dlp acquisition failure, browser-cookie fallback boundaries, and local output permission/path failures.
- **FR-015**: The repository MUST include deterministic tests for prerequisite/configuration validation, setup/launch command construction or diagnostics, version metadata, and artifact-safety rules without requiring YouTube access, model downloads, or Apple Silicon CI hardware.
- **FR-016**: The release candidate MUST include a documented local Apple Silicon smoke procedure using the approved public test video and an explicit small model, while clearly separating that evidence from deterministic CI.
- **FR-017**: The repository MUST include a versioned GitHub Release plan covering tag/version alignment, release notes, source archive contents, verification evidence, and rollback/withdrawal guidance; implementation MUST NOT publish the actual GitHub Release automatically.
- **FR-018**: Reviewable repository and release artifacts MUST exclude cookies, credentials, browser profiles, private media, generated private transcripts, model caches, and accidental machine-specific absolute paths.
- **FR-019**: v1.0 MUST NOT add hosted processing, public tunnels, paid API fallbacks, accounts, databases, telemetry, playlist batch transcription, summarization, diarization, or timestamps.
- **FR-020**: The chosen v1.0 distribution path MUST be documented as source release plus setup/launch scripts; a signed/notarized packaged macOS application is explicitly deferred to a separate product decision.

### Key Entities

- **Release Configuration**: The supported host/runtime prerequisites, pinned dependency inputs, default model, local directories, loopback behavior, and version value needed to install and launch one release.
- **Local Runtime Artifact**: A project environment, model cache, acquired audio file, temporary run directory, transcript, log, or other local output with an explicit owner, location, retention, and privacy boundary.
- **Release Candidate**: A versioned source snapshot plus review evidence, deterministic test results, Apple Silicon smoke result, artifact-safety inspection, and release notes prepared for but not yet published as a GitHub Release.

## Success Criteria

### Measurable Outcomes

- **SC-001**: On a clean supported Apple Silicon environment with network access and prerequisites available, a new user following only the release documentation can complete setup and reach the local GUI without modifying source files; deterministic setup-path tests cover the documented success and prerequisite-failure branches, including a clean PATH with no global `yt-dlp` while the project `.venv/bin/yt-dlp` remains usable.
- **SC-002**: The documented launch path binds only to `127.0.0.1`, creates no public share/tunnel, and passes the existing GUI privacy contract tests plus the v1.0 configuration tests.
- **SC-003**: The public test video completes the documented small-model Apple Silicon smoke path and produces a non-empty UTF-8 Taiwan Traditional Chinese Markdown transcript while leaving the current-run audio directory empty.
- **SC-004**: The deterministic repository suite remains green on the CI-supported Python version, and the release candidate records the exact commit and CI run used for review.
- **SC-005**: A release-candidate artifact inspection finds zero cookies, credentials, browser profiles, downloaded media, private transcripts, model caches, and machine-specific absolute paths in tracked/release files.
- **SC-006**: A maintainer can identify the exact v1.0 version, setup command, launch command, cleanup boundaries, troubleshooting entry, smoke evidence, and deferred packaged-app decision from the published repository documentation without consulting this conversation.

## Assumptions

- Users have a Mac with Apple Silicon, a supported macOS version, network access for initial dependency/model acquisition, and permission to install local software.
- A supported native Python interpreter and Homebrew/`ffmpeg` are prerequisites; v1.0 may diagnose missing prerequisites but does not silently elevate privileges or install an unrelated package manager.
- If browser login, browser-cookie access, Keychain approval, or a macOS privacy/permission prompt is required, the user must approve it locally; release paths must never bypass the prompt, capture the secret, or copy credentials into the checkout.
- The release is source-based and assumes the user can run documented Terminal commands; a signed/notarized `.app` is out of scope for this feature.
- YouTube availability, yt-dlp behavior, browser-cookie requirements, and model download time can vary; the release must document these as external dependencies rather than promise universal acquisition success.
- The approved v0.1-v0.4 code and privacy boundaries are the baseline; this feature may add release ergonomics but may not weaken those contracts.
- A GitHub Release will be created only after a separate explicit acceptance of the v1.0 release candidate.

## Out of Scope

- Signed or notarized `.app`, DMG, PKG, Homebrew formula, or background login item.
- Windows, Linux, Intel macOS, hosted inference, public tunnels, paid APIs, accounts, database storage, telemetry, playlist processing, summarization, diarization, timestamps, or browser automation beyond the already documented cookie fallback.
- Publishing or editing the actual GitHub Release as part of implementation.
