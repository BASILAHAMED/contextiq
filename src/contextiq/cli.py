from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .exporters import export_result
from .pipeline import default_config, run_ingest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="contextiq", description="Turn messy files into agent-ready context.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help="Ingest a directory of files.")
    ingest.add_argument("path", help="Root directory to ingest")
    ingest.add_argument("--out", required=True, help="Output directory")
    ingest.add_argument("--include-ext", help="Comma-separated file extensions to include")
    ingest.add_argument("--exclude-glob", help="Comma-separated glob patterns to exclude")
    ingest.add_argument("--chunk-size", type=int, default=1200, help="Target chunk size in characters")
    ingest.add_argument("--chunk-overlap", type=int, default=150, help="Chunk overlap in characters")
    ingest.add_argument("--formats", default="jsonl,markdown", help="Comma-separated output formats")
    ingest.add_argument("--fail-on-warning", action="store_true", help="Exit non-zero if warnings occur")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "ingest":
        return 1

    root = Path(args.path).resolve()
    out_dir = Path(args.out).resolve()
    config = default_config(root, out_dir)

    if args.include_ext:
        config.include_extensions = {normalize_extension(ext) for ext in args.include_ext.split(",") if ext.strip()}
    if args.exclude_glob:
        config.exclude_globs = [item.strip() for item in args.exclude_glob.split(",") if item.strip()]
    config.chunk_size = args.chunk_size
    config.chunk_overlap = args.chunk_overlap
    config.formats = {item.strip().lower() for item in args.formats.split(",") if item.strip()}
    config.fail_on_warning = args.fail_on_warning

    result = run_ingest(config)
    export_result(out_dir, result, root, config.formats, config.to_manifest_config())

    print(f"Ingested {len(result.documents)} documents into {len(result.chunks)} chunks.")
    if result.warnings:
        print(f"Warnings: {len(result.warnings)}")
    print(f"Output: {out_dir}")
    return 0


def normalize_extension(extension: str) -> str:
    ext = extension.strip().lower()
    if not ext:
        return ext
    return ext if ext.startswith(".") else f".{ext}"


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
