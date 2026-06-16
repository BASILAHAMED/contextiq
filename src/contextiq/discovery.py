from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_EXTENSIONS = {
    ".txt",
    ".md",
    ".rst",
    ".json",
    ".jsonl",
    ".csv",
    ".tsv",
    ".html",
    ".htm",
    ".pdf",
    ".docx",
}

DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
}


@dataclass(slots=True)
class DiscoveryConfig:
    include_extensions: set[str]
    exclude_globs: list[str]


def iter_files(root: Path, config: DiscoveryConfig) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        if config.include_extensions and path.suffix.lower() not in config.include_extensions:
            continue
        if any(path.match(pattern) for pattern in config.exclude_globs):
            continue
        yield path
