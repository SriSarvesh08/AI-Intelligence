# Runbook

## Setup
1. Ensure Python 3.9+ is installed.
2. Navigate to the `backend` directory.
3. Install dependencies (e.g., `pip install -r requirements.txt`).
4. Copy `.env.example` to `.env` and fill in your Gemini API Key and GitHub Token.

## Running the Server
Run the FastAPI development server:
```bash
uvicorn app.main:app --reload
```
The server will start on `http://127.0.0.1:8000`.

## Testing
- You can access the interactive Swagger UI documentation at `http://127.0.0.1:8000/docs`.
- Check the health of the service at `http://127.0.0.1:8000/health`.

## Export Outputs
When you hit the `/export/json` or `/export/csv` routes, check the `output/` directory (created automatically at the root of `backend`) for the exported files.
