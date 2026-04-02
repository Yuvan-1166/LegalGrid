# Smart Legal System - Backend

RAG-powered legal AI system for Indian law analysis.

## Quick Start

### 1. Setup Environment

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (already done with uv)
uv sync
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your GROQ API key
# Get free API key from: https://console.groq.com
```

### 3. Start Qdrant Vector Database

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or using Docker directly
docker run -d -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant:v1.10.0

# Verify Qdrant is running
curl http://localhost:6333/health
```

### 4. Initialize Database & Seed Data

```bash
# Run seed script to create collections and add sample documents
python scripts/seed_data.py
```

### 5. Start Backend Server

```bash
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test API

```bash
# Health check
curl http://localhost:8000/health

# API documentation (Swagger UI)
open http://localhost:8000/docs
```

## API Endpoints

### Core Endpoints
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Qdrant Management
- `POST /api/v1/qdrant/initialize` - Initialize collections
- `POST /api/v1/qdrant/add-document` - Add document to vector DB
- `POST /api/v1/qdrant/search` - Search documents
- `POST /api/v1/qdrant/clear-cache` - Clear retrieval cache

### Contract Analysis
- `POST /api/v1/contracts/analyze` - Analyze contract text
- `POST /api/v1/contracts/analyze-file` - Analyze uploaded contract file (PDF/TXT)

## Project Structure

```
backend/
├── app/
│   ├── agents/          # Specialized AI agents
│   │   └── contract_agent.py
│   ├── api/             # API routes
│   │   └── routes/
│   │       ├── contracts.py
│   │       └── qdrant.py
│   ├── core/            # Core configurations
│   │   ├── config.py
│   │   └── llm.py
│   ├── models/          # Pydantic schemas
│   │   └── schemas.py
│   └── rag/             # RAG components
│       └── retriever.py
├── scripts/             # Utility scripts
│   └── seed_data.py
├── tests/               # Test files
├── main.py              # FastAPI application
├── docker-compose.yml   # Docker services
└── .env                 # Environment variables
```

## Development

### Adding New Documents

```python
from app.rag.retriever import retriever

retriever.add_document(
    doc_id="unique_id",
    title="Document Title",
    content="Full document text...",
    collection="statutes",  # or "cases", "regulations", "contracts"
    jurisdiction="All-India",
    metadata={"year": 2024, "tags": ["tag1", "tag2"]}
)
```

### Testing Contract Analysis

```bash
curl -X POST http://localhost:8000/api/v1/contracts/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "contract_text": "This agreement is made between Party A and Party B...",
    "jurisdiction": "All-India"
  }'
```

## Next Steps

### Deployment

Ready to deploy? See our comprehensive deployment guides:

- **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** - Start here! Overview of all options
- **[RENDER_FREE_DEPLOYMENT.md](RENDER_FREE_DEPLOYMENT.md)** - Deploy for $0/month (no card required)
- **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** - Production deployment with Blueprint
- **[DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md)** - Quick comparison of options
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Ensure nothing is missed
- **[DEPLOYMENT_ARCHITECTURE.md](DEPLOYMENT_ARCHITECTURE.md)** - System architecture diagrams

Quick deploy:
```bash
./deploy_render.sh  # Validates your setup
# Then follow RENDER_FREE_DEPLOYMENT.md or RENDER_DEPLOYMENT.md
```

### Development

1. Add more legal documents to the corpus (see `INDIAN_LEGAL_DATA_SOURCES.md`)
2. Implement remaining agents (case law, compliance, mediation)
3. Add comprehensive tests
4. Deploy to production

## Troubleshooting

### Qdrant Connection Error
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Restart Qdrant
docker-compose restart qdrant
```

### GROQ API Error
- Verify API key in `.env` file
- Check rate limits at https://console.groq.com

### Import Errors
```bash
# Reinstall dependencies
uv sync --reinstall
```
