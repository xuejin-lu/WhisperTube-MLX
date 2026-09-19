# v1.0 Release Candidate Plan

This document prepares a versioned source release. It does not publish, edit, or create a GitHub Release.

## Candidate identity

- Planned tag for the current candidate: `v1.0.0`.
- [ ] `VERSION` matches `whispertube.version.__version__` and the planned tag `v<version>`.
- [ ] The candidate commit is pushed and the repository is clean.
- [ ] Release notes name the supported native Apple Silicon/macOS 14+ scope and the source-release + setup/launch-script distribution path.
- [ ] The deferred signed/notarized `.app` decision is stated explicitly.

## Verification evidence

- [ ] Deterministic suite passes on the CI-supported Python version; record the exact commit and CI run.
- [ ] Focused release/configuration/artifact tests pass.
- [ ] Local Apple Silicon smoke uses the approved public test video and explicit `mlx-community/whisper-tiny` model.
- [ ] Smoke evidence records non-empty UTF-8 Taiwan Traditional Chinese Markdown, current-run audio cleanup, loopback-only binding, and no public share URL without committing media or transcript contents.
- [ ] Large-v3 remains the documented default; no claim is made about unmeasured large-v3 performance.

## Artifact and privacy inspection

- [ ] Tracked files and the source archive contain no cookies, browser profiles, credentials, downloaded media, private transcripts, model caches, or accidental machine-specific absolute paths.
- [ ] `.venv/`, `temp/`, `outputs/`, and model-cache paths remain outside the reviewable source artifact.
- [ ] README, troubleshooting, quickstart, and release notes agree on setup, launch, cache, cleanup, and Human Gate boundaries.

## Publication action — separate final approval

Only after repository review explicitly approves the candidate may the maintainer create the `v<version>` tag and GitHub Release with the reviewed notes. GitHub's generated source archives are the initial release assets; no model weights, credentials, private media, or private transcripts may be attached.

If a published candidate must be withdrawn, mark the GitHub Release as unavailable according to repository policy, document the reason, and prepare a corrected version rather than mutating the reviewed source snapshot.
