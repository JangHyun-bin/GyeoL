from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "dist" / "gyeol.zip"

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "out",
    "tmp",
}

EXCLUDED_SUFFIXES = {
    ".log",
    ".pyc",
    ".pyo",
    ".pdf",
    ".pptx",
    ".zip",
}

EXCLUDED_NAMES = {
    ".DS_Store",
    "Thumbs.db",
}


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def _should_include(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    parts = set(relative.parts)
    if parts.intersection(EXCLUDED_DIRS):
        return False
    if path.name in EXCLUDED_NAMES:
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return True


def iter_package_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and _should_include(path))


def build_zip(out: Path) -> int:
    out = out if out.is_absolute() else ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()

    files = iter_package_files()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())

    print(f"OK: wrote {_display(out)}")
    print(f"OK: packaged {len(files)} file(s)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Package Gyeol as a portable skill ZIP")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output ZIP path")
    args = parser.parse_args(argv)
    return build_zip(Path(args.out))


if __name__ == "__main__":
    raise SystemExit(main())
