"""
Гибкий сплиттер для RAG: выбирает стратегию по типу файла.
- plain/HTML   → RecursiveCharacterTextSplitter
- Markdown     → MarkdownHeaderTextSplitter  ➜ затем Recursive
- Fallback     → SentenceTransformersTokenTextSplitter
"""

from pathlib import Path
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_text_splitters.sentence_transformers import (
    SentenceTransformersTokenTextSplitter,
)
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

DEFAULT_CHUNK = 400
OVERLAP = 40


def _strip_html(html: str) -> str:
    return BeautifulSoup(html, "lxml").get_text(" ")


def _token_splitter(max_len=DEFAULT_CHUNK, overlap=OVERLAP):
    return SentenceTransformersTokenTextSplitter.from_huggingface_tokenizer(
        tokenizer=SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        ).tokenizer,
        chunk_size=max_len,
        chunk_overlap=overlap,
    )


def split_text(text: str, file_path: str | Path | None = None) -> List[str]:
    """Разбивает текст на чанки с учётом типа документа."""
    suffix = Path(file_path).suffix.lower() if file_path else ""
    chunks: List[str]

    if suffix == ".md":
        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=["#", "##", "###"],
        )
        chunks = md_splitter.split_text(text)
    elif suffix in {".html", ".htm"}:
        clean = _strip_html(text)
        base = RecursiveCharacterTextSplitter(
            chunk_size=DEFAULT_CHUNK,
            chunk_overlap=OVERLAP,
        )
        chunks = base.split_text(clean)
    else:
        splitter = _token_splitter()
        chunks = splitter.split_text(text)
        if len(chunks) == 1 and len(chunks[0].split()) > DEFAULT_CHUNK * 2:
            rc = RecursiveCharacterTextSplitter(
                chunk_size=DEFAULT_CHUNK,
                chunk_overlap=OVERLAP,
            )
            chunks = rc.split_text(text)

    return [c.strip() for c in chunks if len(c.strip()) > 30]
