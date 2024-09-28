from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from dotenv import load_dotenv
import sqlite3

from hackyeah.hackyeah import HackYeahClient, hack_yeah_chain

load_dotenv()


class QuestionRequest(BaseModel):
    question: str


class FirstRequest(BaseModel):
    url: str
    question: str


app = FastAPI()

session_id = 1

DATABASE_NAME = "sessions.db"


def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


init_db()


@app.post("/first_message")
async def first_message(data: FirstRequest):
    hack_yeah_client = HackYeahClient(
        url=data.url, chain=hack_yeah_chain, session_id=session_id
    )
    try:
        res = hack_yeah_client.find_url(data.question)

        if res is None:
            raise HTTPException(
                status_code=404, detail="No relevant information found."
            )

        save_to_db(question=data.question, content=res.content, session_id=session_id)

        return {"result": res.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def save_to_db(question: str, content: str, session_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (session_id, question, content) VALUES (?, ?, ?)",
        (session_id, question, content),
    )
    conn.commit()
    conn.close()


@app.post("/message")
async def message(data: QuestionRequest):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT question, content FROM sessions WHERE session_id = ?", (session_id,)
        )
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Session session_id not found.")

        question, content = row

        return {"question": question, "content": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET endpoint for health check
@app.get("/health")
async def health():
    return {"status": "Healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
