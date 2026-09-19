# Release Contracts

## `whispertube.release`

### Version contract

- `VERSION` contains one semantic version string such as `1.0.0` with a trailing newline.
- `whispertube.version.__version__` equals the stripped `VERSION` value.
- `python -m whispertube.release --version` prints only the version and exits successfully.

### Host check contract

`check_host(facts)` returns a deterministic report with `ok`, stable failure codes, and user-safe remediation text. The supported report requires:

- `system == "Darwin"`;
- `machine == "arm64"`;
- `macos_version >= 14.0`;
- Python major/minor in the supported project range;
- Python executable architecture `arm64`;
- an `ffmpeg` executable discoverable on `PATH`.

The check must not execute arbitrary user input, inspect cookies, or mutate the filesystem.

### CLI diagnostic contract

`python -m whispertube.release --check` exits `0` only when all required checks pass. It exits nonzero with a stable, actionable error line for each missing/unsupported prerequisite. It must be safe to run in CI and on unsupported hosts without importing MLX.

## `scripts/setup_macos.sh`

- Must be invoked from any current directory and locate its project root from the script path.
- Must use the project root's `.venv` and tracked requirement files.
- Must call the host diagnostic before installing Apple Silicon dependencies.
- May create/reuse `.venv`; may install or update only packages inside it.
- Must not use `sudo`, install Homebrew, read/export cookies, delete runtime roots, delete model caches, or overwrite user output.
- Must return nonzero when a prerequisite or dependency install fails.
- Must be idempotent when run against a complete `.venv`.

## `scripts/launch_macos.sh`

- Must locate the same project root and `.venv` as setup.
- Must fail with a setup hint when `.venv/bin/python` is absent.
- Must invoke `python -m whispertube.gui` with user-provided arguments unchanged after the launcher options.
- Must not add `--share`, a non-loopback server name, or broad file-serving paths.

## Documentation contract

README and troubleshooting docs must provide:

1. supported hardware/OS/Python prerequisites;
2. setup and launch commands;
3. default and smoke model behavior;
4. local output and cache boundaries;
5. error diagnosis and browser-cookie fallback warning;
6. uninstall/cleanup boundaries;
7. a link to the pre-publication release checklist.

## Artifact-safety contract

Release inspection must reject tracked/release files containing cookie/profile names, credential material, runtime media extensions, private transcript output, model-cache directories, or machine-specific absolute paths under `/Users/` except approved documentation examples that use placeholders.
