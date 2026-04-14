# Secure API Gateway Prototype

A lightweight, developer-friendly secure API gateway built with Python and FastAPI. It enforces modern security practices like JWT authentication, token-bucket based rate limiting, robust request validation, and structured audit logging before traffic reaches simulated backend services.

## Architecture

Client Request -> [ FastAPI Gateway ] -> [ Validation Chain ] -> [ Mock Backend ]

**Validation Chain:** CORS -> Rate Limiter (100 req/min) -> JWT Auth & RBAC -> Pydantic Schema Validator -> Structured JSON Logger

## Features
- **JWT Authentication**: Validates `Authorization: Bearer <token>`, signatures, expiry, and basic roles.
- **Rate Limiting**: Defends against abuse with memory-backed rate limits via `slowapi`. Configurable limits.
- **Request Validation**: String sanitization and schema enforcement to reject malformed/malicious payloads.
- **Security Logging**: Tracks auth failures, rate limit hits, and data accepted using JSON formatted logs via `structlog`.

## Quick Start
1. Ensure Docker is installed.
2. Clone the repository and copy `.env.example` to `.env`.
3. Start the application:
   ```bash
   docker compose up --build
   ```
4. Access the API Documentation:
   http://localhost:8000/docs
5. Test using the mock user: `username: user, password: user123`

## Development
To run locally without Docker:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.main:app --reload
```

Run tests using pytest:
```bash
pytest tests/
```
