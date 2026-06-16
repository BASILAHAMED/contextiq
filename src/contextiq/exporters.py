from __future__ import annotations

import datetime as dt
from pathlib import Path

from .models import Chunk, IngestResult
from .utils import ensure_dir, write_json, write_jsonl


def export_result(
    out_dir: Path,
    result: IngestResult,
    source_root: Path,
    formats: set[str],
    config: dict,
) -> None:
    ensure_dir(out_dir)
    write_jsonl(out_dir / "documents.jsonl", (doc.to_dict() for doc in result.documents))
    write_jsonl(out_dir / "chunks.jsonl", (chunk.to_dict() for chunk in result.chunks))

    if "markdown" in formats:
        _write_markdown(out_dir / "chunks.md", result.chunks)

    manifest = {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "source_root": str(source_root),
        "summary": result.summary(),
        "warnings": result.warnings,
        "config": config,
    }
    write_json(out_dir / "manifest.json", manifest)


def _write_markdown(path: Path, chunks: list[Chunk]) -> None:
    lines = ["# ContextIQ Chunk Export", ""]
    for chunk in chunks:
        lines.append(f"## {chunk.chunk_id}")
        lines.append("")
        lines.append(f"- Source: `{chunk.source_path}`")
        lines.append(f"- Document: `{chunk.doc_id}`")
        lines.append(f"- Range: `{chunk.start_char}:{chunk.end_char}`")
        if chunk.section_title:
            lines.append(f"- Section: `{chunk.section_title}`")
        lines.append("")
        lines.append(chunk.text)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
