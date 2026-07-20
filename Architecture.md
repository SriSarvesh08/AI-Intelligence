# Technical Architecture Document (Phase VI)

## 1. Scale Strategy (500k+ Records)
To effectively ingest 500,000 startups, products, and research papers without manual intervention, the system employs a heavily concurrent, horizontally scalable architecture:
- **Async Connectors**: Network I/O is completely unblocked using `httpx` async clients combined with `asyncio.gather` for extreme concurrency.
- **Distributed Background Workers**: FastAPI's `BackgroundTasks` queue offloads the scraping processes from the main event loop. In production, this can seamlessly transition to Celery/RabbitMQ with distributed worker nodes.
- **Checkpointing & Pagination**: The `IngestionManager` tracks state continuously (records processed, current page). If the server restarts, workers automatically resume from the last successful checkpoint instead of starting over.

## 2. Handling 413s & 429s (Rate Limits & Context Windows)
Operating at scale against protective APIs (GitHub, ArXiv, Gemini) requires aggressive resilience strategies:
- **429 Too Many Requests**: The pipeline incorporates robust Exponential Backoff coupled with Random Jitter (`delay = (2 ** attempt) + random.uniform(0, 1)`). This prevents the "Thundering Herd" problem when thousands of concurrent connections are instantly retrying.
- **413 Payload Too Large**: To handle massive text payloads crossing the LLM Context Window limit, our `TextChunker` breaks documents into 15k-token semantic segments. If an LLM tier still hits a 413 limit, the payload undergoes an **Intelligent Truncation**. The system automatically halves the prompt size to preserve semantically dense content and gracefully retries on the next fallback tier.
- **Multi-Tier Fallback Chain**: If the primary Gemini Pro model continually fails, the system cascades down the chain (`Gemini Flash -> Groq Llama 3 -> DeepSeek`), ensuring data extraction never permanently halts.

## 3. Freshness Tracking (24-Hour Signal Monitoring)
To ensure we process highly dynamic jobs and news signals and never scrape the same article twice:
- **Canonical Deduplication**: Our Deterministic Entity Resolution engine deduplicates raw entities against a seed list (or Canonical Database).
- **Temporal Checksum Hashing**: Every ingested URL or primary key is hashed alongside its `updated_at` or publication timestamp. We use bloom filters (or Redis caches in production) to perform $O(1)$ lookups. If the hash hasn't changed, the article is completely skipped in the pipeline.
- **Relative Date Normalization**: Our LLM Extraction tier specifically normalizes relative unstructured dates ("2 hours ago") into exact ISO-8601 timestamps, enforcing our 24-hour SLA cutoff dynamically.

## 4. Storage Strategy
- **Primary Database (SQLite)**: SQLite serves as an excellent portable DB for this trial deployment, offering transactional integrity for ingestion tracking, logging, and persisting the canonicalized models without overhead.
- **Transition to Vector / Graph Storage**: As the scale exceeds millions of records with deep relationship mappings (e.g. tracking Research Papers -> GitHub Repos -> Company Startups -> Job Postings), standard RDBMS tables struggle with multi-hop recursive queries. Moving forward, a Graph Database (like Neo4j) will act as the canonical entity mapping storage, while a Vector DB (like Pinecone/Qdrant) will store the embedded semantic chunks for similarity grouping and deduplication clustering.
