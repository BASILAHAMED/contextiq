import json

from contextiq.pipeline import default_config, run_ingest


def test_pipeline_ingests_directory(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("# Title\n\nHello world\n\nSecond paragraph", encoding="utf-8")
    (docs / "b.txt").write_text("Plain text document", encoding="utf-8")
    (docs / "data.json").write_text(json.dumps({"name": "contextiq", "kind": "demo"}), encoding="utf-8")

    out_dir = tmp_path / "out"
    config = default_config(docs, out_dir)

    result = run_ingest(config)

    assert len(result.documents) == 3
    assert len(result.chunks) >= 3
    assert result.warnings == []
