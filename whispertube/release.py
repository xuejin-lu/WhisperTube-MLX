"""Pure release configuration and prerequisite diagnostics."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Iterable

from whispertube.version import __version__


DEFAULT_MODEL = "mlx-community/whisper-large-v3-mlx"
SMOKE_MODEL = "mlx-community/whisper-tiny"
LOOPBACK_HOST = "127.0.0.1"
MIN_MACOS_VERSION = (14, 0)
MIN_PYTHON_VERSION = (3, 10)
_APPROVED_RUNTIME_ROOTS = {"temp", "outputs"}


@dataclass(frozen=True)
class HostFacts:
    system: str
    machine: str
    macos_version: str
    python_version: tuple[int, int]
    python_machine: str
    ffmpeg_path: str | None


@dataclass(frozen=True)
class HostCheckReport:
    ok: bool
    codes: tuple[str, ...]
    message: str


@dataclass(frozen=True)
class ReleaseConfiguration:
    project_root: Path
    venv_path: Path
    default_model: str = DEFAULT_MODEL
    smoke_model: str = SMOKE_MODEL
    loopback_host: str = LOOPBACK_HOST
    audio_root: Path = Path("temp")
    output_root: Path = Path("outputs")


def _version_tuple(value: str) -> tuple[int, int]:
    parts = value.split(".")
    try:
        return int(parts[0]), int(parts[1])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"invalid macOS version: {value!r}") from exc


def check_host(facts: HostFacts) -> HostCheckReport:
    codes: list[str] = []
    messages: list[str] = []
    if facts.system != "Darwin":
        codes.append("HOST_OS")
        messages.append("v1.0 requires macOS on Apple Silicon")
    if facts.machine != "arm64":
        codes.append("HOST_ARCHITECTURE")
        messages.append("run a native arm64 Python environment on Apple Silicon")
    if _version_tuple(facts.macos_version) < MIN_MACOS_VERSION:
        codes.append("MACOS_VERSION")
        messages.append("macOS 14.0 or later is required for the v1.0 MLX path")
    if facts.python_version < MIN_PYTHON_VERSION:
        codes.append("PYTHON_VERSION")
        messages.append("Python 3.10 or later is required")
    if facts.python_machine != "arm64":
        codes.append("PYTHON_ARCHITECTURE")
        messages.append("Python must be native arm64, not x86_64 under Rosetta")
    if not facts.ffmpeg_path:
        codes.append("FFMPEG_MISSING")
        messages.append("install ffmpeg (for example, with Homebrew) and retry")
    if codes:
        return HostCheckReport(False, tuple(codes), "; ".join(messages))
    return HostCheckReport(True, (), "supported native Apple Silicon prerequisites detected")


def collect_host_facts() -> HostFacts:
    macos_version = "0.0"
    if platform.system() == "Darwin":
        completed = subprocess.run(
            ["sw_vers", "-productVersion"],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode == 0:
            macos_version = completed.stdout.strip()
    return HostFacts(
        system=platform.system(),
        machine=platform.machine(),
        macos_version=macos_version,
        python_version=sys.version_info[:2],
        python_machine=platform.machine(),
        ffmpeg_path=shutil.which("ffmpeg"),
    )


def release_configuration(project_root: Path) -> ReleaseConfiguration:
    root = Path(project_root)
    return ReleaseConfiguration(project_root=root, venv_path=root / ".venv")


def approved_runtime_path(value: str | Path) -> Path:
    path = Path(os.path.normpath(str(value)))
    if path.is_absolute() or not path.parts or path.parts[0] not in _APPROVED_RUNTIME_ROOTS:
        raise ValueError("runtime path must remain under temp/ or outputs/")
    if ".." in path.parts:
        raise ValueError("runtime path must not escape its approved root")
    return path


def inspect_artifacts(root: Path, relative_paths: Iterable[str]) -> tuple[str, ...]:
    """Return privacy violations found in a candidate's tracked artifact paths/content."""

    violations: list[str] = []
    media_suffixes = {".webm", ".wav", ".mp3", ".m4a", ".opus", ".flac"}
    forbidden_names = {"cookies.txt", "credentials", "browser-profile"}
    root = Path(root).resolve()
    for relative in relative_paths:
        path = Path(relative)
        if path.name in forbidden_names or path.suffix.lower() in {".cookie", ".cookies"}:
            violations.append(f"private filename: {relative}")
        if path.suffix.lower() in media_suffixes:
            violations.append(f"downloaded media: {relative}")
        if ".cache" in path.parts or "models" in path.parts:
            violations.append(f"runtime cache path: {relative}")
        absolute = root / path
        if not absolute.is_file():
            continue
        text = absolute.read_text(encoding="utf-8", errors="ignore")
        if str(root) in text:
            violations.append(f"machine-specific path: {relative}")
        if "BEGIN " + "PRIVATE KEY" in text:
            violations.append(f"private key material: {relative}")
    return tuple(violations)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WhisperTube-MLX release diagnostics")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--version", action="store_true")
    group.add_argument("--check", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.version:
        print(__version__)
        return 0
    report = check_host(collect_host_facts())
    if report.ok:
        print(f"OK: {report.message}")
        return 0
    print("ERROR: " + report.message, file=sys.stderr)
    print("ERROR CODES: " + ", ".join(report.codes), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
