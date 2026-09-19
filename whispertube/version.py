"""Project version metadata shared by release diagnostics and documentation."""

from pathlib import Path


_VERSION_FILE = Path(__file__).resolve().parents[1] / "VERSION"
__version__ = _VERSION_FILE.read_text(encoding="utf-8").strip()
