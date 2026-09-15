# Project Status

## Current milestone

**v0.1 — Local YouTube audio acquisition**

## Verified

- Public GitHub repository exists: `xuejin-lu/WhisperTube-MLX`.
- Repository currently has a Python `.gitignore`, MIT license, README, and project workflow/spec files.
- Local clone exists on the maintainer's Mac under:
  `~/Developer/xuejin-lu/WhisperTube-MLX`
- Git working tree was clean immediately after cloning.
- The project decision is to run YouTube acquisition locally on the Mac rather than from Colab/datacenter IPs.
- The repository ignores cookies, local media, temp/output folders, and common model/cache artifacts.
- Single-video URL normalization is implemented for watch URLs, `youtu.be`, Shorts, and playlist-bearing watch URLs.
- The local CLI builds a `yt-dlp --no-playlist --format bestaudio/best` command and supports `--cookies-from-browser`.
- Unit tests cover URL normalization and command construction without requiring a live YouTube request.
- Spec Kit v1.0.3 is bootstrapped with a constitution and the v0.1 feature artifacts under `specs/001-local-youtube-audio/`.
- The reviewer-owned security checklist has 12/12 requirements-quality items reviewed and checked.
- Local `yt-dlp 2026.08.19` and `ffmpeg 9.0.1` are callable on the development Mac.
- Anonymous smoke acquisition of the test video succeeded with `[download] 100%` and created one ignored `.webm` file under `temp/audio/`.
- No cookie export or repository credential file was created; the browser-cookie fallback was not needed for this successful anonymous run.
- GitHub Actions deterministic CI passed for commit `4508b08` (run `35019349622`).

## Review findings

v0.1 is **not yet approved for closure**. Repository review found two spec/implementation gaps that must be converged before moving to v0.2:

1. **Relative output path traversal**: `_validate_output_dir()` currently checks only the first lexical path component. A path such as `temp/../../outside` still begins with `temp` and can escape the ignored runtime root after normalization. This violates FR-010's requirement that repository-relative runtime output remain under documented ignored roots.
2. **Audio-only format contract mismatch**: FR-003 requires the highest-quality audio-only representation, while the implementation/tests currently use `bestaudio/best`. The `/best` fallback can select a non-audio-only representation. The next convergence pass must either enforce `bestaudio` or explicitly change the specification and acceptance criteria to permit a muxed fallback, with rationale.

## Not yet verified

- Whether `--cookies-from-browser safari` is needed or works on the maintainer's machine.
- MLX Whisper has not yet been selected/verified in this repository.
- Whether a JavaScript runtime is needed for future YouTube videos or formats; the current smoke run emitted a yt-dlp warning but succeeded.

## Current blocker

The two review findings above block v0.1 approval. They are deterministic and should be resolved autonomously by Codex through Spec Kit convergence and TDD; no maintainer command-running or human authorization is required.

## Next task

Run a v0.1 Spec Kit convergence pass for the two review findings above, then implement the resulting corrective tasks with TDD:

- add RED tests proving relative path traversal such as `temp/../../outside` cannot escape ignored runtime roots;
- fix output-path validation using normalized/resolved containment semantics appropriate for repository-relative paths;
- reconcile FR-003 with downloader format selection and add/adjust tests for the chosen contract;
- run the focused and full deterministic suites, local smoke test where behavior changed, CI, and `$speckit-converge`;
- push the resulting commit(s) and request review again.

Do **not** start v0.2 Whisper work until v0.1 is approved.

## Test video

`https://www.youtube.com/watch?v=gmj41fQTbfY`
