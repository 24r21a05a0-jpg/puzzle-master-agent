import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI(title="Riddle Master")


# -------------------------
# Gemini AI
# -------------------------
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.8
)


class PuzzleRequest(BaseModel):
    difficulty: str = "easy"


# -------------------------
# Home Page
# -------------------------
@app.get("/", response_class=HTMLResponse)
async def home():

    return """
<!DOCTYPE html>
<html>

<head>

<title>🧩 Riddle Master</title>

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<style>

body {
    margin: 0;
    min-height: 100vh;
    font-family: Arial, sans-serif;

    background:
    linear-gradient(
        135deg,
        #667eea,
        #764ba2
    );

    display: flex;
    justify-content: center;
    align-items: center;
}

.container {

    width: 90%;
    max-width: 600px;

    background: white;

    padding: 30px;

    border-radius: 20px;

    text-align: center;

    box-shadow:
    0 10px 30px
    rgba(0,0,0,0.25);
}

h1 {
    color: #5a3ea6;
    font-size: 35px;
}

h2 {
    color: #333;
}

#riddle {

    font-size: 22px;

    margin: 25px 0;

    line-height: 1.5;
}

input {

    width: 80%;

    padding: 12px;

    border: 2px solid #ddd;

    border-radius: 10px;

    font-size: 16px;
}

button {

    margin: 10px;

    padding: 12px 22px;

    border: none;

    border-radius: 10px;

    background: #667eea;

    color: white;

    font-size: 16px;

    cursor: pointer;
}

button:hover {

    background: #4f63c4;
}

#result {

    margin-top: 20px;

    font-weight: bold;

    font-size: 18px;
}

.score {

    color: #5a3ea6;

    font-size: 20px;
}

</style>

</head>


<body>

<div class="container">

<h1>🧩 Riddle Master</h1>

<p class="score">
🏆 Score:
<span id="score">0</span>
</p>

<h2>🤔 Solve the Riddle</h2>

<p id="riddle">
⏳ Loading riddle...
</p>

<input
    type="text"
    id="answer"
    placeholder="Type your answer..."
>

<br>

<button onclick="checkAnswer()">
✅ Check Answer
</button>

<button onclick="newRiddle()">
🔄 New Riddle
</button>

<p id="result"></p>

</div>


<script>

let currentAnswer = "";

let score = 0;


async function newRiddle() {

    document.getElementById("riddle").innerText =
        "⏳ Creating a new riddle...";

    document.getElementById("result").innerText = "";

    document.getElementById("answer").value = "";


    try {

        const response = await fetch(
            "/generate-puzzle",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    difficulty: "easy"
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Server error"
            );

        }


        document.getElementById(
            "riddle"
        ).innerText = data.riddle;


        currentAnswer =
            data.answer
            .toLowerCase()
            .trim();

    }


    catch (error) {

        console.error(error);

        document.getElementById(
            "riddle"
        ).innerText =
            "❌ Riddle generation failed.";


        document.getElementById(
            "result"
        ).innerText =
            "Error: " + error.message;

    }

}



function checkAnswer() {

    const userAnswer =
        document.getElementById(
            "answer"
        ).value
        .toLowerCase()
        .trim();


    const result =
        document.getElementById(
            "result"
        );


    if (!userAnswer) {

        result.innerText =
            "Please enter an answer 😊";

        return;

    }


    if (userAnswer === currentAnswer) {

        score += 10;


        document.getElementById(
            "score"
        ).innerText = score;


        result.innerText =
            "🎉 Correct! Great job!";

    }

    else {

        result.innerText =
            "❌ Not quite! Try again.";

    }

}


newRiddle();

</script>

</body>

</html>
"""


# -------------------------
# Generate Riddle
# -------------------------
@app.post("/generate-puzzle")
async def generate_puzzle(request: PuzzleRequest):

    try:

        prompt = f"""
Create ONE unique, fun and interesting riddle.

Difficulty: {request.difficulty}

IMPORTANT:
- Do NOT use the keyboard riddle.
- Create a different riddle every time.
- The answer must be simple.
- Make the riddle suitable for a fun puzzle game.

Return ONLY valid JSON:

{{
    "riddle": "your riddle here",
    "answer": "correct answer"
}}

Do not use markdown.
Do not add explanations.
"""

        response = await llm.ainvoke(prompt)

        text = response.content

        if isinstance(text, list):
            text = "".join(str(item) for item in text)

        text = text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        puzzle = json.loads(text)

        return {
            "riddle": puzzle["riddle"],
            "answer": puzzle["answer"]
        }

    except Exception as e:

        print("GEMINI ERROR:", str(e))

        # Different fallback riddles
        fallback_riddles = [
            {
                "riddle": "What has hands but cannot clap?",
                "answer": "clock"
            },
            {
                "riddle": "What gets wetter the more it dries?",
                "answer": "towel"
            },
            {
                "riddle": "What has one eye but cannot see?",
                "answer": "needle"
            },
            {
                "riddle": "What has many teeth but cannot bite?",
                "answer": "comb"
            },
            {
                "riddle": "What can travel around the world while staying in one corner?",
                "answer": "stamp"
            }
        ]

        import random

        puzzle = random.choice(fallback_riddles)

        return puzzle

    try:

        prompt = f"""
Create one fun and interesting riddle.

Difficulty: {request.difficulty}

Return ONLY JSON.

Use exactly this format:

{{
    "riddle": "riddle question",
    "answer": "correct answer"
}}

Do not use markdown.
Do not add explanations.
"""


        response = await llm.ainvoke(prompt)


        text = response.content


        # Sometimes Gemini returns a list
        if isinstance(text, list):

            text = "".join(
                str(item)
                for item in text
            )


        text = text.strip()


        # Remove markdown code fences
        if text.startswith("```"):

            text = text.replace(
                "```json",
                ""
            )

            text = text.replace(
                "```",
                ""
            )

            text = text.strip()


        puzzle = json.loads(text)


        return {

            "riddle":
                puzzle["riddle"],

            "answer":
                puzzle["answer"]

        }


    except Exception as e:

        print(
            "ERROR:",
            str(e)
        )


        # Temporary fallback riddle
        return {

            "riddle":
            "I have keys but no locks. "
            "I have space but no room. "
            "What am I?",

            "answer":
            "keyboard"

        }
