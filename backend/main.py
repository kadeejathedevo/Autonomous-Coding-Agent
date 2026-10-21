from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Create the FastAPI application.
app = FastAPI()


# Allow the frontend to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the data expected from the frontend.
class AgentRequest(BaseModel):
    task: str


# Find the main project directory.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the folder where generated files will be saved.
WORKSPACE = BASE_DIR / "workspace"


# Test whether the backend is running.
@app.get("/")
def home():
    return {
        "message": "Autonomous Coding Agent API is running!"
    }


# Generate code based on the user's task.
def generate_code(task: str):

    if "calculator" in task.lower():

        filename = "calculator.py"

        code = '''def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b


print("Calculator")
print("Addition:", add(10, 5))
print("Subtraction:", subtract(10, 5))
print("Multiplication:", multiply(10, 5))
print("Division:", divide(10, 5))
'''

        return filename, code

    # We only support calculator tasks for now.
    raise HTTPException(
        status_code=400,
        detail="Currently, I can only generate a calculator."
    )


# Create a file and write the generated code into it.
def create_file(filename: str, code: str):

    # Ensure the workspace folder exists.
    WORKSPACE.mkdir(exist_ok=True)

    # Create the file path.
    file_path = WORKSPACE / filename

    # Save the generated code.
    file_path.write_text(code, encoding="utf-8")

    return file_path


# Receive a task from the frontend.
@app.post("/agent")
def run_agent(request: AgentRequest):

    # Extract the task text.
    task = request.task.strip()

    # Check whether the user entered a task.
    if not task:
        raise HTTPException(
            status_code=400,
            detail="Please enter a task."
        )

    # Step 1: Generate the code.
    filename, code = generate_code(task)

    # Step 2: Create the file.
    file_path = create_file(filename, code)

    # Step 3: Return the result to the frontend.
    return {
        "message": f"File created successfully: {filename}",
        "status": "created",
        "filename": filename,
        "code": code,
        "path": str(file_path.relative_to(BASE_DIR))
    }