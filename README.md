# Customer Support Agent

An AI-powered customer support agent built with **LangGraph**, **LangChain**, **FastAPI**, and **LangSmith**.

## Architecture

```
POST /chat  (UserInput JSON)
    │
    ▼
input_guard.py          ← blocks injection / abuse before graph starts
    │
    ▼
graph/builder.py        ← StateGraph kicks off
    │
    ├─▶  enrich_query.py      LLM structured-output call
    │         UserInput  ──►  CustomerQuery  (validated by Pydantic)
    │
    ├─▶  route_priority.py    conditional edge
    │         priority == "high"  ──►  create_ticket.py  ──►  SupportTicket
    │         priority != "high"  ──►  faq_lookup.py     ──►  List[FAQResult]
    │
    └─▶  compose_response.py  final LLM call, builds plain-English reply
    │
    ▼
output_guard.py         ← scrub PII, tone check
    │
    ▼
Response JSON  →  caller
```

## Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) installed

### Setup

```bash
# Clone the repo
git clone <repo-url>
cd customer-support-agent

# Install dependencies with uv
make install

# Copy and fill in environment variables
cp .env.example .env
# Edit .env with your OPENAI_API_KEY etc.

# Run the server
make run
```

The API will be available at `http://localhost:8000`.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/chat` | Submit a support query |
| GET | `/health` | Liveness probe |
| GET | `/ready` | Readiness probe |
| POST | `/feedback` | Submit run feedback |

### Example Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: changeme-secret-key" \
  -d '{
    "message": "My order has not arrived and it has been 2 weeks!",
    "user_id": "user_123",
    "session_id": "sess_abc"
  }'
```

### Example Response

```json
{
  "response": "I'm sorry to hear your order hasn't arrived...",
  "priority": "high",
  "ticket_id": "TICKET-20240101-abc123",
  "run_id": "uuid-...",
  "session_id": "sess_abc"
}
```

## Development

```bash
# Run tests
make test

# Lint
make lint

# Format code
make format

# Type check
make typecheck
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `API_KEY` | Yes | Bearer token for API authentication |
| `LANGCHAIN_API_KEY` | No | LangSmith API key for tracing |
| `LANGCHAIN_TRACING_V2` | No | Enable LangSmith tracing |
| `MODEL_NAME` | No | OpenAI model (default: `gpt-4o-mini`) |
| `POSTGRES_DSN` | No | PostgreSQL DSN for persistent checkpointing |
