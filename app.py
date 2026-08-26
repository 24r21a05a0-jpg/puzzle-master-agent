import os
import json
import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI


app = FastAPI(title="Riddle Master")


# =========================================================
# GEMINI AI
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("WARNING: GEMINI_API_KEY is not set.")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=1.0
)


# =========================================================
# REQUEST MODEL
# =========================================================

class PuzzleRequest(BaseModel):
    difficulty: str = "easy"
    previous_riddle: str = ""


# =========================================================
# FALLBACK RIDDLES
# =========================================================

fallback_riddles = [
    {
        "riddle": "What has hands but cannot clap?",
        "answer": "clock",
        "hint": "It tells you the time."
    },
    {
        "riddle": "What gets wetter the more it dries?",
        "answer": "towel",
        "hint": "You use it after a bath."
    },
    {
        "riddle": "What has one eye but cannot see?",
        "answer": "needle",
        "hint": "It is used for sewing."
    },
    {
        "riddle": "What has many teeth but cannot bite?",
        "answer": "comb",
        "hint": "You use it on your hair."
    },
    {
        "riddle": "What has a neck but no head?",
        "answer": "bottle",
        "hint": "You can drink from it."
    },
    {
        "riddle": "What has legs but cannot walk?",
        "answer": "table",
        "hint": "You can eat at it."
    },
    {
        "riddle": "What goes up but never comes down?",
        "answer": "age",
        "hint": "It increases as you grow older."
    },
    {
        "riddle": "What has words but never speaks?",
        "answer": "book",
        "hint": "You can read it."
    },
    {
        "riddle": "What has a face and hands but no arms?",
        "answer": "clock",
        "hint": "It helps you know the time."
    },
    {
        "riddle": "What can you catch but never throw?",
        "answer": "cold",
        "hint": "You might get it when you are sick."
    },
    {
        "riddle": "What has a thumb and four fingers but is not alive?",
        "answer": "glove",
        "hint": "You wear it on your hand."
    },
    {
        "riddle": "What has a head and a tail but no body?",
        "answer": "coin",
        "hint": "You can use it to pay."
    },
    {
        "riddle": "What has cities but no houses, forests but no trees, and rivers but no water?",
        "answer": "map",
        "hint": "You use it to find places."
    },
    {
        "riddle": "What has four legs in the morning, two at noon, and three in the evening?",
        "answer": "human",
        "hint": "Think about the stages of life."
    },
    {
        "riddle": "What is full of holes but still holds water?",
        "answer": "sponge",
        "hint": "You might use it to clean dishes."
    },
    {
        "riddle": "What belongs to you but other people use it more than you?",
        "answer": "name",
        "hint": "People call you by it."
    },
    {
        "riddle": "What has keys but cannot open locks?",
        "answer": "piano",
        "hint": "You can play music on it."
    },
    {
        "riddle": "What can run but never walks?",
        "answer": "water",
        "hint": "It flows in rivers."
    },
    {
        "riddle": "What has an eye but cannot see and is often found in a storm?",
        "answer": "hurricane",
        "hint": "It is a powerful weather event."
    },
    {
        "riddle": "What is always in front of you but cannot be seen?",
        "answer": "future",
        "hint": "It has not happened yet."
    },
    {
        "riddle": "What comes down but never goes up?",
        "answer": "rain",
        "hint": "You may need an umbrella."
    },
    {
        "riddle": "What has a ring but no finger?",
        "answer": "telephone",
        "hint": "It can make a ringing sound."
    },
    {
        "riddle": "What has branches but no fruit, trunk, or leaves?",
        "answer": "bank",
        "hint": "You may keep money there."
    },
    {
        "riddle": "What has a bed but never sleeps?",
        "answer": "river",
        "hint": "Water flows through it."
    },
    {
        "riddle": "What has a bark but no bite?",
        "answer": "tree",
        "hint": "It grows in forests."
    },
    {
        "riddle": "What is easy to lift but hard to throw?",
        "answer": "feather",
        "hint": "It is very light."
    },
    {
        "riddle": "What has ears but cannot hear?",
        "answer": "corn",
        "hint": "It is a type of food."
    },
    {
        "riddle": "What has a bottom at the top?",
        "answer": "leg",
        "hint": "Think about a part of your body."
    },
    {
        "riddle": "What can fill a room but takes up no space?",
        "answer": "light",
        "hint": "You need it to see."
    },
    {
        "riddle": "What has no life but can die?",
        "answer": "battery",
        "hint": "It provides power to devices."
    }
]


# =========================================================
# HOME PAGE
# =========================================================

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

* {
    box-sizing: border-box;
}

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

    padding: 20px;
}


.container {

    width: 100%;

    max-width: 650px;

    background: white;

    padding: 35px;

    border-radius: 25px;

    text-align: center;

    box-shadow:
    0 15px 40px
    rgba(0,0,0,0.25);
}


h1 {

    color: #5a3ea6;

    font-size: 38px;

    margin-bottom: 5px;
}


.subtitle {

    color: #777;

    margin-bottom: 20px;
}


.stats {

    display: flex;

    justify-content: space-around;

    margin: 20px 0;

    font-size: 18px;

    font-weight: bold;
}


.riddle-box {

    background: #f5f3ff;

    padding: 25px;

    border-radius: 18px;

    margin: 25px 0;
}


#riddle {

    font-size: 23px;

    line-height: 1.6;

    color: #333;
}


select {

    padding: 10px;

    border-radius: 10px;

    border: 2px solid #ddd;

    font-size: 16px;

    margin-bottom: 15px;
}


input {

    width: 90%;

    padding: 14px;

    border: 2px solid #ddd;

    border-radius: 12px;

    font-size: 17px;

    outline: none;
}


input:focus {

    border-color: #667eea;
}


button {

    margin: 8px;

    padding: 13px 20px;

    border: none;

    border-radius: 12px;

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

    font-size: 19px;

    font-weight: bold;
}


#hint {

    margin-top: 15px;

    color: #e67e22;

    font-weight: bold;
}


.footer {

    margin-top: 25px;

    color: #999;

    font-size: 13px;
}

</style>

</head>


<body>


<div class="container">


<h1>🧩 Riddle Master</h1>


<p class="subtitle">
Think smart. Solve riddles. Have fun!
</p>


<div class="stats">

<span>
🏆 Score:
<span id="score">0</span>
</span>

<span>
❤️ Lives:
<span id="lives">3</span>
</span>

</div>


<label>
Difficulty:
</label>


<select id="difficulty">

<option value="easy">Easy</option>

<option value="medium">Medium</option>

<option value="hard">Hard</option>

</select>


<div class="riddle-box">

<h2>🤔 Solve the Riddle</h2>

<p id="riddle">
⏳ Creating your riddle...
</p>

</div>


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


<button onclick="showHint()">
💡 Hint
</button>


<p id="hint"></p>


<p id="result"></p>


<p class="footer">
🤖 Powered by Gemini AI
</p>


</div>


<script>

let currentAnswer = "";

let currentHint = "";

let currentRiddle = "";

let score = 0;

let lives = 3;


async function newRiddle() {

    document.getElementById("riddle").innerText =
        "⏳ Creating a new riddle...";

    document.getElementById("result").innerText = "";

    document.getElementById("hint").innerText = "";

    document.getElementById("answer").value = "";


    const difficulty =
        document.getElementById("difficulty").value;


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

                    difficulty: difficulty,

                    previous_riddle:
                        currentRiddle

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


        currentRiddle =
            data.riddle;


        currentAnswer =
            data.answer
            .toLowerCase()
            .trim();


        currentHint =
            data.hint || "";


        document.getElementById("riddle")
        .innerText =
            currentRiddle;


    }

    catch (error) {

        console.error(error);


        document.getElementById("riddle")
        .innerText =
            "❌ Could not generate riddle.";


        document.getElementById("result")
        .innerText =
            "Please try again.";


    }

}


function checkAnswer() {

    const userAnswer =
        document.getElementById("answer")
        .value
        .toLowerCase()
        .trim();


    const result =
        document.getElementById("result");


    if (!userAnswer) {

        result.innerText =
            "Please enter an answer 😊";

        return;

    }


    if (userAnswer === currentAnswer) {

        score += 10;


        document.getElementById("score")
        .innerText =
            score;


        result.innerText =
            "🎉 Correct! Excellent!";


    }

    else {

        lives--;


        document.getElementById("lives")
        .innerText =
            lives;


        result.innerText =
            "❌ Not correct. Try again!";


        if (lives <= 0) {

            result.innerText =
                "😢 Game over! Click New Riddle to continue.";

            currentAnswer = "";

        }

    }

}


function showHint() {

    if (currentHint) {

        document.getElementById("hint")
        .innerText =
            "💡 Hint: " + currentHint;

    }

    else {

        document.getElementById("hint")
        .innerText =
            "💡 No hint available.";

    }

}


document.getElementById("difficulty")
.addEventListener(
    "change",
    newRiddle
);


newRiddle();

</script>


</body>

</html>
"""


# =========================================================
# GENERATE PUZZLE
# =========================================================

@app.post("/generate-puzzle")
async def generate_puzzle(
    request: PuzzleRequest
):

    try:

        prompt = f"""
Create ONE completely new and interesting riddle.

Difficulty: {request.difficulty}

Previous riddle:
{request.previous_riddle}

IMPORTANT RULES:

1. Do NOT repeat the previous riddle.
2. Do NOT use the keyboard riddle.
3. Create a fresh riddle.
4. The answer should be clear.
5. Make it fun for a puzzle game.
6. Include a short hint.
7. Return ONLY valid JSON.

Return exactly:

{{
    "riddle": "riddle question",
    "answer": "correct answer",
    "hint": "short hint"
}}

Do not use markdown.
Do not add explanations.
"""


        response = await llm.ainvoke(prompt)


        text = response.content


        if isinstance(text, list):

            text = "".join(
                str(item)
                for item in text
            )


        text = text.strip()


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


        riddle = puzzle.get("riddle")
        answer = puzzle.get("answer")
        hint = puzzle.get("hint", "Think carefully!")


        if not riddle or not answer:

            raise ValueError(
                "Invalid Gemini response"
            )


        return {

            "riddle": riddle,

            "answer": answer,

            "hint": hint

        }


    except Exception as e:

        print(
            "GEMINI ERROR:",
            str(e)
        )


        # Random fallback
        puzzle = random.choice(
            fallback_riddles
        )


        return {

            "riddle":
                puzzle["riddle"],

            "answer":
                puzzle["answer"],

            "hint":
                puzzle["hint"]

        }

