from __future__ import annotations

import ollama
from app.embeddings_qdrant import embed_text, load_vector_store
from app.history import log_message

SYSTEM_PROMPT = (
    "You are an internal documentation assistant. "
    "Answer only from the provided context. "
    "If the answer is not present, reply that you don't know."
    "Your name - Support"
)


class RagEngine:
    def __init__(self, k: int = 5, model: str = "llama3"):
        self.k = k
        self.model = model
        self.vs = load_vector_store()

    async def answer(
        self, question: str, session_id: str | None = None
    ) -> str:
        session_id = session_id or "anon"
        log_message(session_id, "user", question)

        if not question.strip():
            answer = "Question is empty."
            log_message(session_id, "bot", answer)
            return answer

        q_vec = embed_text(question)
        docs = self.vs.similarity_search_by_vector(q_vec, k=self.k)
        context = "\n".join(docs)

        if not context:
            answer = "I don't know — no relevant content in the KB yet."
            log_message(session_id, "bot", answer)
            return answer

        prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
        try:
            resp = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            answer = resp["message"]["content"].strip()
        except Exception as e:
            answer = f"LLM error: {e}"

        log_message(session_id, "bot", answer)
        return answer
