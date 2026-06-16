from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chunking import chunk_document
from .discovery import DEFAULT_EXTENSIONS, DiscoveryConfig, iter_files
from .loaders import load_document
from .models import IngestResult


@dataclass(slots=True)
class IngestConfig:
    root: Path
    output_dir: Path
    include_extensions: set[str]
    exclude_globs: list[str]
    chunk_size: int
    chunk_overlap: int
    formats: set[str]
    fail_on_warning: bool = False

    def to_manifest_config(self) -> dict:
        return {
            "include_extensions": sorted(self.include_extensions),
            "exclude_globs": self.exclude_globs,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "formats": sorted(self.formats),
            "fail_on_warning": self.fail_on_warning,
        }


def default_config(root: Path, output_dir: Path) -> IngestConfig:
    return IngestConfig(
        root=root,
        output_dir=output_dir,
        include_extensions=set(DEFAULT_EXTENSIONS),
        exclude_globs=[],
        chunk_size=1200,
        chunk_overlap=150,
        formats={"jsonl", "markdown"},
        fail_on_warning=False,
    )


def run_ingest(config: IngestConfig) -> IngestResult:
    discovery = DiscoveryConfig(
        include_extensions={ext.lower() for ext in config.include_extensions},
        exclude_globs=config.exclude_globs,
    )
    documents = []
    chunks = []
    warnings: list[str] = []

    for path in iter_files(config.root, discovery):
        document = load_document(path, config.root)
        if not document.text:
            warnings.extend(f"{document.source_path}: {warning}" for warning in document.warnings)
            documents.append(document)
            continue

        documents.append(document)
        warnings.extend(f"{document.source_path}: {warning}" for warning in document.warnings)
        chunks.extend(chunk_document(document, config.chunk_size, config.chunk_overlap))

    if config.fail_on_warning and warnings:
        raise ValueError("Warnings encountered during ingest:\n" + "\n".join(warnings))

    return IngestResult(documents=documents, chunks=chunks, warnings=warnings)
