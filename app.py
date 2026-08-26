from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Puzzle Master Agent is running!"}
