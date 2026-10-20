from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500",
    "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    task: str


@app.get("/")
def home():
    return {"message": "Autonomous Coding Agent API is running!"}


@app.post("/agent")
def agent(request: AgentRequest):
    task = request.task
    # Here you can implement the logic to handle the task
    return {"message": f"Your Task was received: {task}",
            "status": "successfully received"
            }
