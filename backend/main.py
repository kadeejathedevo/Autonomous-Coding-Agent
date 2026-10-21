from pathlib import Path
import os
import re
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai


# ----------------------------------
# 1. Project paths and environment
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None


# ----------------------------------
# 2. Create FastAPI application
# ----------------------------------

app = FastAPI(
    title="Autonomous Coding Agent",
    description="An AI agent that generates Python code from tasks.",
    version="1.0"
)


# ----------------------------------
# 3. Allow frontend communication
# ----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------
# 4. Incoming request
# ----------------------------------

class AgentRequest(BaseModel):
    task: str


# ----------------------------------
# 5. Workspace folder
# ----------------------------------

WORKSPACE = BASE_DIR / "workspace"


# ----------------------------------
# 6. Root route
# ----------------------------------

@app.get("/")
def home():
    return {
        "message": "Autonomous Coding Agent API is running!"
    }


# ----------------------------------
# 7. Generate code using Gemini
# ----------------------------------

def generate_code(task: str):

    if client is None:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is missing. Check your .env file."
        )

    prompt = f"""
You are a Python coding assistant.

Generate a complete Python program for this task:

{task}

Instructions:
- Return only Python source code.
- Do not include explanations.
- Do not use Markdown code fences.
- Make the program complete and runnable.
- Do not include code that deletes files or accesses secrets.
"""

    try:

        # Ask Gemini to generate code
        response = client.interactions.create(
            model=MODEL,
            input=prompt,
        )

        code = response.output_text

        if not code:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response."
            )

        code = code.strip()

        # Remove Markdown code fences
        code = re.sub(
            r"^```(?:python)?\s*",
            "",
            code,
            flags=re.IGNORECASE
        )

        code = re.sub(
            r"\s*```$",
            "",
            code
        )

        # Return the generated code
        return code

    except HTTPException:
        raise

    except Exception as error:

        print("Gemini generation error:", error)

        raise HTTPException(
            status_code=502,
            detail="Gemini could not generate code. Check your API key, model and quota."
        )


# ----------------------------------
# 8. Create a different file
#    for every generated program
# ----------------------------------

def create_file(code: str):

    # Create workspace if it does not exist
    WORKSPACE.mkdir(
        parents=True,
        exist_ok=True
    )

    # Generate a unique ID for this file
    unique_id = uuid.uuid4().hex[:8]

    # Create a unique filename
    filename = f"generated_{unique_id}.py"

    # Create the full file path
    file_path = WORKSPACE / filename

    # Save the generated code
    file_path.write_text(
        code,
        encoding="utf-8"
    )

    return filename, file_path


# ----------------------------------
# 9. Main agent endpoint
# ----------------------------------

@app.post("/agent")
def run_agent(request: AgentRequest):

    task = request.task.strip()

    if not task:
        raise HTTPException(
            status_code=400,
            detail="Please enter a task."
        )

    # Generate code
    code = generate_code(task)

    # Save in a new file
    filename, file_path = create_file(code)

    # Send the code and filename to frontend
    return {
        "message": f"File created successfully: {filename}",
        "status": "created",
        "filename": filename,
        "code": code,
        "path": str(file_path.relative_to(BASE_DIR))
    }