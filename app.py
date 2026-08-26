```python
import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI(title="Puzzle Master Agent")

# Gemini AI
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)


# Request model
class PuzzleRequest(BaseModel):
    puzzle_type: str
    difficulty: str


# Home page
@app.get("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧩 Riddle Master</title>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;
                font-family: Arial, sans-serif;
                background: linear-gradient(
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
                max-width: 650px;
                background: white;
                padding: 40px;
                border-radius: 25px;
                text-align: center;
                box-shadow: 0 15px 40px rgba(0,0,0,0.25);
            }

            h1 {
                font-size: 38px;
                margin-bottom: 10px;
                color: #333;
            }

            .subtitle {
                color: #666;
                font-size: 18px;
                margin-bottom: 30px;
            }

            .difficulty {
                margin-bottom: 20px;
            }

            select {
                padding: 12px 20px;
                border-radius: 10px;
                border: 2px solid #ddd;
                font-size: 16px;
                cursor: pointer;
            }

            button {
                padding: 14px 25px;
                margin: 10px;
                border: none;
                border-radius: 12px;
                background: #667eea;
                color: white;
                font-size: 17px;
                font-weight: bold;
                cursor: pointer;
            }

            button:hover {
                transform: scale(1.03);
                opacity: 0.9;
            }

            .riddle-box {
                margin-top: 25px;
                padding: 25px;
                background: #f5f5f5;
                border-radius: 15px;
                min-height: 120px;
                text-align: left;
                line-height: 1.6;
                white-space: pre-wrap;
            }

            #status {
                margin-top: 15px;
                color: #666;
            }

        </style>
    </head>

    <body>

        <div class="container">

            <h1>🧩 Riddle Master</h1>

            <p class="subtitle">
                Challenge your brain with an AI-generated riddle!
            </p>

            <div class="difficulty">

                <label>
                    <b>Choose Difficulty:</b>
                </label>

                <br><br>

                <select id="difficulty">

                    <option value="easy">
                        Easy
                    </option>

                    <option value="medium">
                        Medium
                    </option>

                    <option value="hard">
                        Hard
                    </option>

                </select>

            </div>

            <button onclick="generateRiddle()">
                🎲 Generate Riddle
            </button>

            <div id="riddle" class="riddle-box">
                🤔 Your riddle will appear here...
            </div>

            <p id="status"></p>

        </div>


        <script>

            async function generateRiddle() {

                const difficulty =
                    document.getElementById("difficulty").value;

                const riddleBox =
                    document.getElementById("riddle");

                const status =
                    document.getElementById("status");

                riddleBox.innerText =
                    "🤖 Creating your riddle...";

                status.innerText = "";

                try {

                    const response =
                        await fetch("/generate-puzzle", {

                            method: "POST",

                            headers: {
                                "Content-Type": "application/json"
                            },

                            body: JSON.stringify({

                                puzzle_type: "riddle",

                                difficulty: difficulty

                            })

                        });


                    const data =
                        await response.json();


                    if (response.ok) {

                        riddleBox.innerText =
                            data.puzzle;

                        status.innerText =
                            "🎉 Good luck!";

                    }

                    else {

                        riddleBox.innerText =
                            "❌ Something went wrong.";

                    }

                }

                catch (error) {

                    riddleBox.innerText =
                        "❌ Could not connect to the server.";

                    status.innerText =
                        "Please try again.";

                }

            }

        </script>

    </body>

    </html>
    """


# Generate puzzle
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
        "puzzle": str(response.content)
    }
```
