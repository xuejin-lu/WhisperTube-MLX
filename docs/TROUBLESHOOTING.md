# Troubleshooting

WhisperTube-MLX v1.0 runs locally on a native Apple Silicon Mac. The diagnostic command is:

```bash
./.venv/bin/python -m whispertube.release --check
```

## Unsupported Mac, OS, or Python

The supported path is Apple Silicon (`arm64`) on macOS 14 or later with native Python 3.10 or later. If `uname -m` or `python3 -c 'import platform; print(platform.machine())'` reports `x86_64`, the process is running on Intel or through Rosetta. Install or select a native Apple Silicon Python and rerun setup. The release does not attempt to make MLX run on an unsupported architecture.

## Missing `ffmpeg`

The local decoder must be available on `PATH`. Install it through the package manager approved by the Mac owner, for example:

```bash
brew install ffmpeg
```

Then rerun `./scripts/setup_macos.sh`. Setup does not install Homebrew, use `sudo`, or change unrelated system packages.

## Dependency installation failure

Setup uses the project-local `.venv` and pinned requirement files. Read the first failing package message, verify network access, and rerun setup. An interrupted environment is not deleted automatically; if `.venv/bin/python` is absent, move that disposable environment aside only after confirming it contains no user data, then rerun setup. Do not delete `outputs/`, model caches, cookies, or browser profiles as a dependency-repair step.

## Model download or cache failure

The normal target is `mlx-community/whisper-large-v3-mlx`; the first use may download model weights locally and can take substantial time and disk space. For a constrained validation, pass `--model mlx-community/whisper-tiny`. Check network access and available disk space. Model caches may be outside the checkout and are not bundled, inspected for contents, or deleted by setup/launch scripts.

## YouTube and yt-dlp failures

YouTube availability and `yt-dlp` behavior can change. Read the cause-specific acquisition error and retry with the same public URL later. A missing JavaScript runtime warning may be non-fatal for some videos. If the video requires browser access, use the documented browser cookie fallback `--cookies-from-browser safari` locally; do not export `cookies.txt`, copy a browser profile, or paste credentials into the repository. Browser login or cookie access may require a user-owned browser prompt.

## Keychain or macOS permission prompts

If macOS, the browser, or Keychain asks for privacy/permission approval, the user must approve or deny it locally. The release scripts never bypass prompts, capture secrets, or copy credentials. This is the only kind of setup interruption that requires a human action; ordinary shell commands and retries remain agent/user-run according to the workflow.

## Output and permission failures

Keep audio and transcript directories under the documented ignored `temp/` and `outputs/` roots. A path outside those roots is rejected. Current-run acquired audio is cleaned according to the pipeline contract; a retained Markdown transcript is not deleted as cleanup. Check that the checkout is writable and that no ambient Gradio file-serving configuration is broadening the GUI's approved boundary.

## Uninstall and cleanup

To uninstall the project environment, remove only the disposable project-local `.venv/` after stopping the GUI. Review `outputs/` for transcripts before removing it, and review `temp/` for any intentionally retained local artifacts. Model caches may live outside the checkout and are not removed by the release scripts; remove a model cache only when you explicitly choose to reclaim that disk space. Never remove browser profiles, cookies, or credentials as part of routine project cleanup.
