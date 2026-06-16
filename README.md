# ContextIQ

ContextIQ turns messy files into agent-ready context.

It is a local-first ingestion pipeline for developers building RAG systems, agent memory layers, document search, and eval datasets. Point it at a folder and it produces clean JSONL and Markdown exports with chunked, traceable content.

## Why it exists

Most AI tooling starts after your data is already clean. Real projects get stuck much earlier:

- PDFs are noisy
- Word docs lose structure
- repos and notes mix formats
- chunks are inconsistent
- source traceability is easy to lose

ContextIQ focuses on the missing middle: consistent ingestion, chunking, and export.

## Features

- Local-first CLI
- Recursive file ingestion
- Built-in support for:
  - `.txt`, `.md`, `.rst`
  - `.json`, `.jsonl`
  - `.csv`, `.tsv`
  - `.html`, `.htm`
  - optional `.pdf` via `pypdf`
  - optional `.docx` via `python-docx`
- Document-aware chunking
- Source-preserving metadata
- JSONL and Markdown exports
- Run manifest with counts, warnings, and timings

## Quickstart

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
contextiq ingest ./examples --out ./build/context
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
contextiq ingest .\examples --out .\build\context
```

## CLI

```bash
contextiq ingest <path> --out <directory>
```

Useful flags:

- `--include-ext .md,.txt,.json`
- `--exclude-glob "*.min.js,*.lock"`
- `--chunk-size 1200`
- `--chunk-overlap 150`
- `--formats jsonl,markdown`
- `--fail-on-warning`

## Output

`contextiq ingest` writes:

- `documents.jsonl`: normalized source documents
- `chunks.jsonl`: chunked outputs for RAG/agents
- `chunks.md`: human-readable review file
- `manifest.json`: summary of the run

Each chunk preserves:

- source path
- document id
- chunk id
- byte and character ranges when available
- headings / section hints

## Example

```bash
contextiq ingest ./docs --out ./dist/context --chunk-size 900 --chunk-overlap 120
```

## Development

```bash
pip install -e .[dev]
pytest
```

## Roadmap

- embeddings plugin interface
- vector DB exporters
- OCR pipeline
- table extraction
- citation-aware retrieval benchmarks
