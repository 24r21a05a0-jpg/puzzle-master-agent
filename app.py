import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI(title="Puzzle Master Agent")

# Gemini AI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)


class PuzzleRequest(BaseModel):
    puzzle_type: str
    difficulty: str


@app.get("/")
def home():
    return {
        "message": "🧩 Puzzle Master Agent is running!"
    }


@app.post("/generate-puzzle")
def generate_puzzle(request: PuzzleRequest):

    prompt = f"""
    You are a Puzzle Master AI.

    Generate ONE {request.difficulty} difficulty
    {request.puzzle_type} puzzle.

    Give:
    1. The puzzle question
    2. The correct answer
    3. A short explanation

    Do not generate multiple puzzles.
    """

    response = llm.invoke(prompt)

    return {
        "puzzle": response.content
    }
