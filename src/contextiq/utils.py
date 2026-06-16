from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable


WHITESPACE_RE = re.compile(r"[ \t]+")
BLANKLINE_RE = re.compile(r"\n{3,}")


def stable_id(*parts: str) -> str:
    joined = "::".join(parts)
    return hashlib.sha1(joined.encode("utf-8")).hexdigest()[:16]


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(WHITESPACE_RE.sub(" ", line).rstrip() for line in text.splitlines())
    return BLANKLINE_RE.sub("\n\n", text).strip()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")
