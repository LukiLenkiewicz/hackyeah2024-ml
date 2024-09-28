from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from dotenv import load_dotenv

from hackyeah.hackyeah import HackYeahClient, hack_yeah_chain

load_dotenv()

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


class FirstRequest(BaseModel):
    url: str
    question: str


@app.post("/first_message")
async def first_message(data: FirstRequest):
    hack_yeah_client = HackYeahClient(url=data.url, chain=hack_yeah_chain)
    try:
        res = hack_yeah_client.find_url(data.question)

        if res is None:
            raise HTTPException(
                status_code=404, detail="No relevant information found."
            )

        return {"result": res.content}

    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


# POST endpoint for processing the request
@app.post("/message")
async def message(data: DetectionRequest):
    try:
        res = find_url(data.url, data.question, data.essa_chain)

        # Check if a valid result was returned
        if res is None:
            raise HTTPException(
                status_code=404, detail="No relevant information found."
            )

        return {"result": res.content}

    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


# GET endpoint for health check
@app.get("/health")
async def health():
    return {"status": "Healthy"}


# Run the FastAPI application with 'uvicorn' if running this file directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
