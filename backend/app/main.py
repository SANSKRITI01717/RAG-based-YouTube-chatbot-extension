from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import (
    get_transcript,
    split_transcript,
    index_video,
    video_exists,
    ask_question
)


app = FastAPI(
    title="YouTube RAG API",
    version="1.0.0"
)


class VideoRequest(BaseModel):
    video_id: str


class QuestionRequest(BaseModel):
    video_id: str
    question: str


@app.get("/")
def home():
    return {
        "message": "YouTube RAG API is running"
    }


@app.post("/process-video")
def process_video(request: VideoRequest):

    video_id = request.video_id

    if video_exists(video_id):
        return {
            "message": "Video already indexed",
            "video_id": video_id
        }

    text = get_transcript(video_id)

    if not text:
        return {
            "error": "Transcript not found"
        }

    chunks = split_transcript(text)

    count = index_video(
        video_id,
        chunks
    )

    return {
        "message": "Video indexed successfully",
        "video_id": video_id,
        "chunks": count
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    answer = ask_question(
        request.video_id,
        request.question
    )

    return {
        "video_id": request.video_id,
        "question": request.question,
        "answer": answer
    }