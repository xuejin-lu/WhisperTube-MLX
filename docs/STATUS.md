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
- The local CLI builds a `yt-dlp --no-playlist --format bestaudio` command and supports `--cookies-from-browser`.
- Unit tests cover URL normalization and command construction without requiring a live YouTube request.
- Relative output traversal such as `temp/../../outside` is rejected before downloader invocation;
  normalized paths remain beneath the documented ignored runtime roots.
- The downloader contract now requests `bestaudio` explicitly, preserving the audio-only boundary
  required by FR-003.
- Spec Kit v1.0.3 is bootstrapped with a constitution and the v0.1 feature artifacts under `specs/001-local-youtube-audio/`.
- The reviewer-owned security checklist has 12/12 requirements-quality items reviewed and checked.
- Local `yt-dlp 2026.08.19` and `ffmpeg 9.0.1` are callable on the development Mac.
- Anonymous smoke acquisition of the test video succeeded with `[download] 100%`, selected yt-dlp
  format `251`, and created one ignored `.webm` audio file under `temp/audio-v0-1-converged/`.
- No cookie export or repository credential file was created; the browser-cookie fallback was not needed for this successful anonymous run.
- GitHub Actions deterministic CI passed for commit `4508b08` (run `35019349622`).

## Review findings

The pre-implementation reviewer identified two deterministic gaps. Both were resolved through
convergence tasks T024-T025 and verified with RED → GREEN tests; no human gate was required.

## Not yet verified

- Whether `--cookies-from-browser safari` is needed or works on the maintainer's machine.
- MLX Whisper has not yet been selected/verified in this repository.
- Whether a JavaScript runtime is needed for future YouTube videos or formats; the current smoke run emitted a yt-dlp warning but succeeded.

## Current blocker

No deterministic v0.1 implementation blocker remains. Browser-session fallback and future MLX
selection remain environment-dependent or explicitly out of v0.1 scope.

## Next task

Run final CI/convergence verification for v0.1, push the completed corrective work, and request
maintainer review. Do not start v0.2 Whisper work until v0.1 is approved.

Do **not** start v0.2 Whisper work until v0.1 is approved.

## Test video

`https://www.youtube.com/watch?v=gmj41fQTbfY`
