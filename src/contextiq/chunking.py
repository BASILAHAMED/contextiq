from __future__ import annotations

from .models import Chunk, Document
from .utils import stable_id


def chunk_document(document: Document, chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    if not document.text:
        return []

    text = document.text
    chunks: list[Chunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = min(len(text), start + chunk_size)
        if end < len(text):
            candidate = text.rfind("\n\n", start, end)
            if candidate > start + max(200, chunk_size // 3):
                end = candidate
            else:
                sentence_break = text.rfind(". ", start, end)
                if sentence_break > start + max(120, chunk_size // 4):
                    end = sentence_break + 1

        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(
                Chunk(
                    chunk_id=stable_id(document.doc_id, str(index), str(start), str(end)),
                    doc_id=document.doc_id,
                    source_path=document.source_path,
                    text=chunk_text,
                    start_char=start,
                    end_char=end,
                    section_title=_resolve_section_title(document, start, end),
                    metadata={"source_type": document.source_type},
                )
            )

        if end >= len(text):
            break

        next_start = max(end - chunk_overlap, start + 1)
        if next_start <= start:
            next_start = end
        start = next_start
        index += 1

    return chunks


def _resolve_section_title(document: Document, start: int, end: int) -> str | None:
    for section in document.sections:
        if section.start_char <= start < section.end_char:
            return section.title
        if start <= section.start_char < end:
            return section.title
    return None
