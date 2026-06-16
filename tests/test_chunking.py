from contextiq.chunking import chunk_document
from contextiq.models import Document


def test_chunk_document_preserves_source_metadata():
    text = "# Intro\n\n" + ("A" * 700) + "\n\n## Details\n\n" + ("B" * 700)
    document = Document(
        doc_id="doc1",
        source_path="notes/sample.md",
        source_type="md",
        text=text,
    )

    chunks = chunk_document(document, chunk_size=800, chunk_overlap=100)

    assert len(chunks) >= 2
    assert all(chunk.doc_id == "doc1" for chunk in chunks)
    assert all(chunk.source_path == "notes/sample.md" for chunk in chunks)
    assert chunks[0].start_char == 0
