from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Section:
    title: str
    level: int
    start_char: int
    end_char: int


@dataclass(slots=True)
class Document:
    doc_id: str
    source_path: str
    source_type: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    sections: list[Section] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["char_count"] = len(self.text)
        return payload


@dataclass(slots=True)
class Chunk:
    chunk_id: str
    doc_id: str
    source_path: str
    text: str
    start_char: int
    end_char: int
    section_title: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["char_count"] = len(self.text)
        return payload


@dataclass(slots=True)
class IngestResult:
    documents: list[Document]
    chunks: list[Chunk]
    warnings: list[str]

    def summary(self) -> dict[str, Any]:
        return {
            "document_count": len(self.documents),
            "chunk_count": len(self.chunks),
            "warning_count": len(self.warnings),
        }
