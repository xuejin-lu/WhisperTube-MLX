# Research: Public Usable Release

## Decision 1: Source release plus scripts for v1.0

**Decision**: Ship a versioned source archive/repository snapshot with `scripts/setup_macos.sh` and `scripts/launch_macos.sh`. Do not add a `.app`, DMG, PKG, Homebrew formula, login item, signing, or notarization in v1.0.

**Rationale**: The product already runs as a Python source tree, and the current milestone has no selected signing/notarization policy. A script-based source release exposes the local dependency boundary, is easy to test in CI with fakes, and avoids a second distribution runtime. GitHub Releases provide a versioned tag, release notes, and downloadable source archive without requiring a custom binary artifact.

**Rejected alternatives**:

- A packaged `.app`/DMG would introduce bundling, code-signing, notarization, update, and model/runtime packaging decisions that are not required to prove public usability.
- A Homebrew formula would create a separate package-maintenance and tap-release surface while still needing Python/MLX and model-cache decisions.
- An auto-installing bootstrapper would need elevated permissions or package-manager policy and would make failure recovery less transparent.

## Decision 2: Built-in `venv` with pinned requirements

**Decision**: Create or reuse a project-local `.venv` with `python3 -m venv`, upgrade only the environment's pip tooling as needed, and install the existing pinned requirement files plus the local downloader dependency. Setup must be rerunnable and must not remove user data.

**Evidence**: Python's official `venv` documentation describes isolated, disposable environments that are not checked into source control and should be recreated rather than moved. This matches the existing `.gitignore` and the need for a clean, inspectable release path.

**Source**: <https://docs.python.org/3/library/venv.html>

**Rejected alternative**: Adding `uv` or Conda could improve installation speed or interpreter management, but it adds another prerequisite and is not needed for the smallest reproducible path. The user can adopt one later as a separate optimization.

## Decision 3: Explicit native Apple Silicon and macOS checks

**Decision**: Before dependency installation, diagnose `Darwin`, `arm64`, a supported macOS baseline, and a native Python interpreter. Fail with a remediation message for Intel or Rosetta/x86_64 Python. Keep the release target explicit rather than attempting a compatibility layer.

**Evidence**: MLX is the Apple machine-learning team's array framework for Apple silicon and its project documentation states macOS installation through the native Python package. MLX's current build configuration requires macOS 14 or later for Metal builds; the release therefore adopts macOS 14+ as its explicit v1.0 baseline.

**Sources**:

- <https://github.com/ml-explore/mlx>
- <https://github.com/ml-explore/mlx/blob/main/CMakeLists.txt>

## Decision 4: `ffmpeg` is a visible prerequisite, not an implicit installer action

**Decision**: Setup checks for `ffmpeg` on `PATH` and reports the supported Homebrew installation command when it is absent. It does not install Homebrew, request `sudo`, or silently change the system package configuration.

**Rationale**: Decoder installation is a system-level boundary and should be explicit. The documented command is easy to verify and keeps setup safe on machines where the user has a different package-management policy.

**Source**: <https://brew.sh/>

## Decision 5: Local model cache is first-use state

**Decision**: Keep `mlx-whisper`'s model download/cache behavior local and document that the first transcription may download a model. The default remains `mlx-community/whisper-large-v3-mlx`; smoke instructions use explicit `mlx-community/whisper-tiny`. Setup does not prefetch or bundle weights and uninstall guidance does not delete caches by default.

**Rationale**: Model weights are large, machine-specific runtime state and may contain user-selected models. Bundling them would make a source release unnecessarily large; automatic deletion could destroy a user's reusable local data.

## Decision 6: Release publication is a separate approval action

**Decision**: Add `docs/RELEASE.md` with tag/version alignment, notes, evidence, artifact inspection, and withdrawal guidance. Implementation may prepare and verify a candidate but must not publish or edit the actual GitHub Release.

**Evidence**: GitHub documents releases as deployable software iterations based on Git tags with notes and optional assets; repository source archives are available from the tagged point. This is sufficient for the v1.0 source distribution plan.

**Source**: <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>

## Open risks retained explicitly

- Anonymous YouTube access may change; browser-cookie fallback remains local and credential-sensitive.
- yt-dlp may warn about a missing JavaScript runtime even when the approved public video succeeds.
- Full large-v3 memory/time cost remains unmeasured; v1.0 smoke evidence uses the small explicit model.
- Gradio remains pinned at 6.27.0 and its loopback/file-serving contract must stay covered by existing tests.
- A future `.app` distribution still needs a separate decision on signing, notarization, entitlements, updates, and model/runtime delivery.
