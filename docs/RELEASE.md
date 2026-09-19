# v1.0 Release Candidate Plan

This document records a versioned source release. The document itself does not publish, edit, or create a GitHub Release.

## Candidate identity

- Planned tag for the current candidate: `v1.0.0`.
- [x] `VERSION` matches `whispertube.version.__version__` and the planned tag `v<version>`.
- [x] The candidate remediation commit is pushed and the repository is clean (exact SHA and CI run are recorded in `docs/STATUS.md` after push).
- [x] Release notes name the supported native Apple Silicon/macOS 14+ scope and the source-release + setup/launch-script distribution path.
- [x] The deferred signed/notarized `.app` decision is stated explicitly.

## Verification evidence

- [x] Deterministic suite passes on the CI-supported Python version; the exact commit and CI run are recorded in `docs/STATUS.md`.
- [x] Focused release/configuration/artifact tests pass, including clean-PATH launcher/setup execution coverage.
- [x] Local Apple Silicon smoke uses the approved public test video and explicit `mlx-community/whisper-tiny` model.
- [x] Smoke evidence records non-empty UTF-8 Taiwan Traditional Chinese Markdown, current-run audio cleanup, loopback-only binding, and no public share URL without committing media or transcript contents.
- [x] Large-v3 remains the documented default; no claim is made about unmeasured large-v3 performance.

## Artifact and privacy inspection

- [x] Tracked files and the source archive contain no cookies, browser profiles, credentials, downloaded media, private transcripts, model caches, or accidental machine-specific absolute paths.
- [x] `.venv/`, `temp/`, `outputs/`, and model-cache paths remain outside the reviewable source artifact.
- [x] README, troubleshooting, quickstart, and release notes agree on setup, launch, cache, cleanup, and Human Gate boundaries.

## Publication action — separate final approval

- [x] Created the `v<version>` tag and published the GitHub Release after explicit repository review approval.

GitHub's generated source archives are the release assets; no model weights, credentials, private media, or private transcripts were attached. This publication checkbox was intentionally separate from the completed implementation and verification checks above.

If a published candidate must be withdrawn, mark the GitHub Release as unavailable according to repository policy, document the reason, and prepare a corrected version rather than mutating the reviewed source snapshot.
