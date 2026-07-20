# API Reference

## Ingestion
- `POST /ingestion/start`: Starts bulk acquisition for specified targets.
- `POST /ingestion/pause`: Pauses the acquisition.
- `POST /ingestion/resume`: Resumes the paused acquisition.
- `POST /ingestion/stop`: Stops the acquisition.
- `GET /ingestion/status`: Retrieves the current state of ingestion.
- `GET /ingestion/statistics`: Retrieves metrics, average speed, success rate, and total records ingested.

## LLM Extraction
- `POST /llm/extract`: Expects `{"text": "...", "source_url": "...", "api_key": "..."}`. Runs chunked extraction with Gemini and returns structured Pydantic-validated JSON.

## Entity Resolution
- `POST /entity-resolution`: Triggers resolution and normalization.
- `GET /entity-resolution/candidates`: Gets candidates for merging.
- `POST /entity-resolution/merge`: Applies a manual merge between two entities.
- `GET /entity-resolution/stats`: Returns current entity counts and stats.

## Validation & Export
- `POST /validation`: Validates extracted entities and generates a validation report.
- `POST /export/json`: Dumps all resolved entities to `output/resolved_entities.json`.
- `POST /export/csv`: Dumps all resolved entities to `output/output.csv`.
