# Autonomous Coding Agent

An AI-powered coding assistant that generates Python code from user instructions.

## Features

- Accepts coding tasks through a web interface.
- Uses Gemini to generate Python code.
- Displays generated code in the frontend.
- Saves generated code as `generated.py` in the workspace folder.
- Uses FastAPI to connect the frontend and AI model.

## Technologies Used

- Python
- FastAPI
- Gemini API
- HTML
- CSS
- JavaScript
- Git and GitHub

## How It Works

1. The user enters a coding task in the frontend.
2. JavaScript sends the task to the FastAPI backend.
3. The backend sends the prompt to Gemini.
4. Gemini returns Python code.
5. The backend saves the code in the workspace.
6. The frontend displays the generated code.

## Setup

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Add your Gemini API key and model name to a `.env` file.
5. Start the backend using `python -m uvicorn backend.main:app --reload`.
6. Open `frontend/index.html` using VS Code Live Server.

## Security Note

Generated code should be reviewed before execution. This project generates and saves code but does not automatically run it.
