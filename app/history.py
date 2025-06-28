from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session, select

engine = create_engine("sqlite:///data/chat.db", echo=False)


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: str
    role: str
    content: str
    ts: datetime = Field(default_factory=datetime.utcnow)


SQLModel.metadata.create_all(engine)


def log_message(session_id, role, content):
    with Session(engine) as s:
        s.add(Message(session_id=session_id, role=role, content=content))
        s.commit()


def get_history(session_id):
    with Session(engine) as s:
        stmt = (
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.ts)
        )
        return s.exec(stmt).all()
