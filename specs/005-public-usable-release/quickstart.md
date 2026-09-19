# Quickstart: Public Usable Release

This is the user-facing path the implementation must make true.

## Supported prerequisites

Use a Mac with Apple Silicon (M1/M2/M3/M4 family), macOS 14 or later, a native Apple Silicon Python 3.10+, Homebrew's `ffmpeg`, and network access for Python packages, yt-dlp acquisition, and first-use model download.

Confirm the machine before setup:

```bash
uname -m
sw_vers -productVersion
python3 -c 'import platform; print(platform.machine())'
ffmpeg -version
```

Expected architecture is `arm64`; Python must not report an x86_64/Rosetta runtime.

## Setup and launch

From the unpacked release directory:

```bash
./scripts/setup_macos.sh
./scripts/launch_macos.sh
```

The setup path creates or reuses `.venv`, installs the pinned local dependencies, and leaves model caches and user output outside its deletion scope. The launch path starts the existing GUI on `127.0.0.1` only.

## First run and smoke run

The normal GUI quality target remains `mlx-community/whisper-large-v3-mlx`; first use may download model weights into the local model cache. For a constrained validation run, pass `--model mlx-community/whisper-tiny` and use an ignored temporary audio/output directory. The smoke procedure must use the approved public test video and record the resulting Markdown path and cleanup evidence without committing the artifacts.

## Cleanup

The project `.venv`, `temp/`, and `outputs/` are local/disposable project artifacts. User transcripts should be reviewed before deletion. Model caches may be outside the project root and are not removed by the setup or launch scripts; remove them only through an explicit user choice.

## Troubleshooting and release review

If setup fails, run `./.venv/bin/python -m whispertube.release --check` when the environment exists and consult `docs/TROUBLESHOOTING.md`. Do not export browser cookies into the repository. Before publication, follow `docs/RELEASE.md`; its candidate checklist is evidence gathering only and does not publish a GitHub Release.
