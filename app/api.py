import traceback

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.rag_engine import RagEngine
from app.history import get_history


app = FastAPI()
engine = RagEngine()


class Query(BaseModel):
    question: str
    session_id: str | None = None


@app.post("/chat")
async def chat(query: Query):
    try:
        ans = await engine.answer(query.question, session_id=query.session_id)
        return {"answer": ans}
    except Exception as exc:
        print("[/chat ERROR]\n", traceback.format_exc())
        raise HTTPException(500, detail=str(exc))


@app.get("/history/{session_id}")
async def history(session_id: str):
    msgs = get_history(session_id)
    return [
        {
            "role": m.role,
            "content": m.content,
            "ts": m.ts.isoformat(),
        }
        for m in msgs
    ]


@app.get("/")
async def root():
    return FileResponse("static/index.html")


app.mount(
    "/static",
    StaticFiles(directory="static", html=True),
    name="static",
)
