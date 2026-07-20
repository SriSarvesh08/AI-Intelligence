# AI Data Intelligence Platform (Backend Only)

A production-ready data ingestion, parsing, LLM extraction, and entity resolution backend API.

## Core Features
- **Data Ingestion**: Async workers pull from arXiv, GitHub, HuggingFace Models, and HuggingFace Datasets into SQLite.
- **Parsing**: Advanced HTML cleaning that removes headers, footers, and ads.
- **LLM Extraction**: Integrates with Gemini with chunking, retries, rate-limit (429/413) handling, and Pydantic validation.
- **Entity Resolution**: Normalizes names, URLs, locations, and deduplicates records.
- **Exporting**: Validates records and exports directly to structured CSV/JSON formats in an `output/` directory.

## Technology Stack
- **FastAPI** for API routing.
- **Uvicorn** for async server.
- **SQLAlchemy** + **SQLite** for database.
- **Pydantic** for schemas and validation.
- **Gemini API** for AI-powered extraction.

See `Runbook.md` for getting started instructions.
