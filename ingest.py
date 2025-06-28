from pathlib import Path

from app.embeddings_qdrant import save_vectors
from app.splitter import split_text

RAW_DIR = Path("data/raw")


def ingest_raw():
    files = list(RAW_DIR.rglob("*.html")) + list(RAW_DIR.rglob("*.md"))
    if not files:
        print("[ingest] Нет файлов в data/raw/ — ничего индексировать")
        return
    for fp in files:
        text = fp.read_text(encoding="utf8")
        chunks = split_text(text)
        save_vectors(chunks)
        print(f"[ingest] {fp} → {len(chunks)} chunks")


if __name__ == "__main__":
    ingest_raw()
