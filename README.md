# LegalGrid - AI-Powered Legal Assistant

> A comprehensive RAG-powered legal AI system for Indian law, featuring contract analysis, case law retrieval, compliance monitoring, dispute mediation, and an intelligent chat assistant.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 19](https://img.shields.io/badge/react-19-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

LegalGrid is a modern, AI-powered legal assistant platform designed specifically for Indian law. It combines advanced RAG (Retrieval-Augmented Generation) technology with specialized AI agents to provide comprehensive legal analysis, research, and consultation services.

### Key Capabilities

- **Contract Analysis**: Automated risk assessment and compliance checking
- **Case Law Research**: Semantic search across Indian legal precedents
- **Compliance Monitoring**: Real-time regulatory compliance tracking
- **Dispute Mediation**: AI-assisted conflict resolution
- **AI Chat Assistant**: ChatGPT-like conversational interface with session management

## ✨ Features

### Implemented Features

#### 🔍 Contract Analysis
- Upload contracts in PDF, TXT, DOC, or DOCX format
- Automated risk identification and red flag detection
- Jurisdiction-specific compliance checking
- Detailed recommendations and remediation steps
- PDF export of analysis reports

#### 📚 Case Law Search
- Semantic search across Supreme Court and High Court judgments
- Precedent strength analysis
- Relevance scoring and ranking
- Citation extraction and linking

#### ⚖️ Compliance Monitoring
- Multi-regulation compliance checking
- Gap analysis and risk assessment
- Regulatory change detection
- Automated compliance reports

#### 🤝 Dispute Mediation
- Multi-party dispute analysis
- Fair outcome recommendations
- Legal precedent integration
- Mediation strategy suggestions

#### 💬 AI Chat Assistant
- ChatGPT-style conversational interface
- Session management with persistent history
- Quick templates for common legal queries
- Document upload and analysis
- Smart follow-up suggestions
- Export conversations

### Technical Features

- **Hybrid RAG System**: Combines semantic (vector) and keyword (BM25) search
- **Vector Database**: Qdrant for efficient similarity search
- **Advanced Embeddings**: sentence-transformers (all-mpnet-base-v2)
- **LLM Integration**: GROQ API for fast inference
- **Session Management**: Persistent chat history with LRU caching
- **Professional UI**: Clean, modern interface inspired by leading SaaS products

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │   Home   │Contracts │Case Law  │Compliance│ AI Chat  │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (Axios)
┌────────────────────────▼────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Routes Layer                         │  │
│  │  /contracts  /cases  /compliance  /disputes  /chat   │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │              AI Agents Layer                          │  │
│  │  Contract │ Case Law │ Compliance │ Mediation Agent  │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │              RAG System                               │  │
│  │  Hybrid Retriever │ Reranker │ BM25 Search           │  │
│  └────────────────────┬─────────────────────────────────┘  │
└───────────────────────┼──────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
   │  GROQ   │    │ Qdrant  │    │  File   │
   │   LLM   │    │ Vector  │    │ Storage │
   │         │    │   DB    │    │         │
   └─────────┘    └─────────┘    └─────────┘
```

### Data Flow

1. **User Request** → Frontend sends request to backend API
2. **API Processing** → FastAPI routes request to appropriate agent
3. **RAG Retrieval** → Agent queries vector DB for relevant documents
4. **LLM Generation** → GROQ generates response with retrieved context
5. **Response** → Formatted response returned to frontend

## 🛠️ Tech Stack

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | FastAPI | High-performance async API |
| LLM | GROQ (Llama 3.1) | Fast inference engine |
| Vector DB | Qdrant | Similarity search |
| Embeddings | sentence-transformers | Document vectorization |
| RAG | LangChain | Retrieval pipeline |
| Search | Whoosh (BM25) | Keyword search |
| Package Manager | uv | Fast Python package management |
| Validation | Pydantic | Data validation |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | React 19 | UI library |
| Build Tool | Vite 8 | Fast bundler |
| Routing | React Router 7 | Client-side routing |
| Styling | TailwindCSS 4 | Utility-first CSS |
| HTTP Client | Axios | API communication |
| Package Manager | pnpm | Fast package management |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Containerization | Docker | Service isolation |
| Vector DB | Qdrant (Docker) | Vector storage |
| Storage | JSON Files | Session persistence |

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python 3.10+** with `uv` package manager
- **Node.js 18+** with `pnpm` package manager
- **Docker** and Docker Compose
- **GROQ API Key** (free from [console.groq.com](https://console.groq.com))

### Installation

#### 1. Clone Repository

```bash
git clone <repository-url>
cd LegalGrid
```

#### 2. Backend Setup

```bash
cd backend

# Activate virtual environment
source .venv/bin/activate

# Configure environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start Qdrant vector database
docker-compose up -d

# Initialize database with sample data
python scripts/seed_data.py

# Start backend server
python main.py
```

Backend will be available at **http://localhost:8000**

API documentation at **http://localhost:8000/docs**

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

Frontend will be available at **http://localhost:5173**

### Verification

1. Open http://localhost:5173 in your browser
2. Navigate to different pages to test features
3. Try the AI Chat assistant at http://localhost:5173/chat
4. Check API docs at http://localhost:8000/docs

## 📁 Project Structure

```
LegalGrid/
├── backend/                          # Backend application
│   ├── app/
│   │   ├── agents/                   # AI agents
│   │   │   ├── case_law_agent.py    # Case law research
│   │   │   ├── compliance_agent.py  # Compliance checking
│   │   │   ├── contract_agent.py    # Contract analysis
│   │   │   └── mediation_agent.py   # Dispute mediation
│   │   ├── api/
│   │   │   └── routes/              # API endpoints
│   │   │       ├── cases.py         # Case law routes
│   │   │       ├── chat.py          # Chat assistant routes
│   │   │       ├── compliance.py    # Compliance routes
│   │   │       ├── contracts.py     # Contract routes
│   │   │       ├── disputes.py      # Dispute routes
│   │   │       └── qdrant.py        # Vector DB routes
│   │   ├── core/                    # Core functionality
│   │   │   ├── cache.py             # Caching layer
│   │   │   ├── config.py            # Configuration
│   │   │   ├── llm.py               # LLM client
│   │   │   ├── logging_config.py    # Logging setup
│   │   │   ├── monitoring.py        # Performance monitoring
│   │   │   ├── rate_limiter.py      # Rate limiting
│   │   │   ├── session_manager.py   # Chat session management
│   │   │   └── validation.py        # Input validation
│   │   ├── models/                  # Data models
│   │   │   ├── chat_session.py      # Chat session models
│   │   │   └── schemas.py           # API schemas
│   │   ├── rag/                     # RAG system
│   │   │   ├── bm25_search.py       # Keyword search
│   │   │   ├── hybrid_retriever.py  # Hybrid search
│   │   │   ├── reranker.py          # Result reranking
│   │   │   └── retriever.py         # Vector retrieval
│   │   ├── scrapers/                # Data scrapers
│   │   │   └── indian_kanoon.py     # Legal data scraper
│   │   └── utils/                   # Utilities
│   │       ├── benchmarks.py        # Performance benchmarks
│   │       ├── chunking.py          # Document chunking
│   │       └── pdf_export.py        # PDF generation
│   ├── data/
│   │   ├── chat_sessions/           # Persistent chat sessions
│   │   └── corpus.jsonl             # Legal corpus
│   ├── scripts/                     # Utility scripts
│   │   ├── bulk_ingest.py           # Bulk data ingestion
│   │   ├── seed_data.py             # Database seeding
│   │   └── evaluate_retrieval.py    # RAG evaluation
│   ├── tests/                       # Test suite
│   ├── whoosh_index/                # BM25 search index
│   ├── main.py                      # Application entry point
│   ├── docker-compose.yml           # Qdrant service
│   ├── Dockerfile                   # Backend container
│   ├── pyproject.toml               # Python dependencies
│   └── .env.example                 # Environment template
│
├── frontend/                        # Frontend application
│   ├── src/
│   │   ├── assets/                  # Static assets
│   │   ├── components/              # Reusable components
│   │   │   ├── Badge.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── ErrorAlert.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   ├── ProgressBar.jsx
│   │   │   ├── SuccessAlert.jsx
│   │   │   └── Tooltip.jsx
│   │   ├── pages/                   # Page components
│   │   │   ├── Home.jsx             # Landing page
│   │   │   ├── ContractAnalysis.jsx # Contract analysis
│   │   │   ├── CaseSearch.jsx       # Case law search
│   │   │   ├── Compliance.jsx       # Compliance checking
│   │   │   ├── Disputes.jsx         # Dispute mediation
│   │   │   └── Chat.jsx             # AI chat assistant
│   │   ├── services/
│   │   │   └── api.js               # API client
│   │   ├── App.jsx                  # Main application
│   │   ├── main.jsx                 # Entry point
│   │   └── index.css                # Global styles
│   ├── public/                      # Public assets
│   ├── package.json                 # Dependencies
│   ├── vite.config.js               # Vite configuration
│   ├── tailwind.config.js           # Tailwind configuration
│   └── Dockerfile                   # Frontend container
│
├── docs/                            # Documentation
│   ├── CHAT_SESSION_GUIDE.md        # Chat feature guide
│   ├── CHAT_QUICKSTART.md           # Chat quick start
│   ├── CHAT_ARCHITECTURE.md         # Chat architecture
│   ├── RAG_IMPLEMENTATION_GUIDE.md  # RAG technical guide
│   └── INDIAN_LEGAL_DATA_SOURCES.md # Data sources
│
├── docker-compose.prod.yml          # Production compose
├── README.md                        # This file
└── .gitignore                       # Git ignore rules
```

## 📡 API Documentation

### Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

### Authentication

Currently, the API does not require authentication. For production deployment, implement JWT or API key authentication.

### Core Endpoints

#### Health Check
```http
GET /health
```

Returns API health status.

#### API Information
```http
GET /
```

Returns API version and available endpoints.

### Contract Analysis

#### Analyze Contract Text
```http
POST /api/v1/contracts/analyze
Content-Type: application/json

{
  "contract_text": "string",
  "jurisdiction": "All-India"
}
```

#### Analyze Contract File
```http
POST /api/v1/contracts/analyze-file
Content-Type: multipart/form-data

file: <binary>
jurisdiction: "All-India"
```

### Case Law Search

#### Search Cases
```http
POST /api/v1/cases/search
Content-Type: application/json

{
  "case_description": "string",
  "jurisdiction": "All-India",
  "top_k": 5
}
```

#### Analyze Precedent Strength
```http
POST /api/v1/cases/analyze-strength
Content-Type: application/json

{
  "case_description": "string",
  "jurisdiction": "All-India",
  "top_k": 5
}
```

### Compliance

#### Check Compliance
```http
POST /api/v1/compliance/check
Content-Type: application/json

{
  "org_profile": "string",
  "regulations": ["string"]
}
```

#### Detect Regulatory Changes
```http
GET /api/v1/compliance/detect-changes/{regulation}
```

### Dispute Mediation

#### Mediate Dispute
```http
POST /api/v1/disputes/mediate
Content-Type: application/json

{
  "dispute": {
    "parties": ["string"],
    "narrative": "string",
    "claims": ["string"],
    "jurisdiction": "All-India"
  }
}
```

### Chat Assistant

#### Send Message
```http
POST /api/v1/chat/message
Content-Type: application/json

{
  "message": "string",
  "session_id": "string" (optional)
}
```

#### Upload Document
```http
POST /api/v1/chat/upload
Content-Type: multipart/form-data

file: <binary>
query: "string" (optional)
session_id: "string" (optional)
```

#### List Sessions
```http
GET /api/v1/chat/sessions?limit=50
```

#### Get Session
```http
GET /api/v1/chat/sessions/{session_id}
```

#### Delete Session
```http
DELETE /api/v1/chat/sessions/{session_id}
```

#### Update Session Title
```http
PATCH /api/v1/chat/sessions/{session_id}/title
Content-Type: application/json

{
  "title": "string"
}
```

### Vector Database

#### Initialize Collections
```http
POST /api/v1/qdrant/initialize
```

#### Search Documents
```http
POST /api/v1/qdrant/search
Content-Type: application/json

{
  "query": "string",
  "collection": "string",
  "jurisdiction": "All-India",
  "top_k": 5
}
```

For complete API documentation with interactive testing, visit `/docs` when the backend is running.

## 💻 Development

### Backend Development

#### Running Tests
```bash
cd backend
source .venv/bin/activate
pytest
```

#### Code Formatting
```bash
black app/
isort app/
```

#### Type Checking
```bash
mypy app/
```

#### Adding Dependencies
```bash
uv add <package-name>
```

### Frontend Development

#### Running Tests
```bash
cd frontend
pnpm test
```

#### Linting
```bash
pnpm lint
```

#### Building
```bash
pnpm build
```

#### Preview Production Build
```bash
pnpm preview
```

### Environment Variables

#### Backend (.env)
```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
DEBUG=true
LOG_LEVEL=INFO
QDRANT_HOST=localhost
QDRANT_PORT=6333
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 🚢 Deployment

### Docker Deployment

#### Build Images
```bash
# Backend
cd backend
docker build -t legalgrid-backend .

# Frontend
cd frontend
docker build -t legalgrid-frontend .
```

#### Run with Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment

#### Backend (Railway/Render)
1. Connect your GitHub repository
2. Set environment variables (GROQ_API_KEY)
3. Deploy from `backend/` directory
4. Ensure Qdrant is accessible (use managed service or separate container)

#### Frontend (Vercel/Netlify)
```bash
cd frontend
pnpm build

# Deploy to Vercel
vercel

# Or deploy to Netlify
netlify deploy --prod --dir=dist
```

### Production Considerations

- Use managed Qdrant service (Qdrant Cloud)
- Implement authentication and authorization
- Add rate limiting and request throttling
- Set up monitoring and logging (Sentry, LogRocket)
- Configure CORS properly
- Use environment-specific configurations
- Implement CI/CD pipeline
- Set up SSL/TLS certificates
- Configure CDN for frontend assets

## 🧪 Testing

### Backend Tests

```bash
cd backend
source .venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_contracts.py

# Run with verbose output
pytest -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
pnpm test

# Run with coverage
pnpm test:coverage

# Run in watch mode
pnpm test:watch
```

### Manual Testing

1. **Contract Analysis**: Upload a sample contract and verify analysis
2. **Case Search**: Search for a legal term and check results
3. **Compliance**: Test compliance checking with sample data
4. **Chat Assistant**: Create sessions, send messages, test persistence
5. **API**: Use Swagger UI at `/docs` to test endpoints

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **JavaScript**: Follow Airbnb style guide, use ESLint
- **Commits**: Use conventional commits (feat:, fix:, docs:, etc.)

### Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure CI/CD pipeline passes
4. Request review from maintainers
5. Address review feedback

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Indian Kanoon** for providing access to Indian legal judgments
- **GROQ** for fast and efficient LLM inference
- **Qdrant** for powerful vector search capabilities
- **LangChain** for RAG framework and agent tools
- **FastAPI** for excellent API framework
- **React** and **Vite** for modern frontend development

## 📞 Support

For questions, issues, or feature requests:

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: support@legalgrid.com

## 🗺️ Roadmap

### Current Version (v1.0)
- ✅ Contract analysis
- ✅ Case law search
- ✅ Compliance monitoring
- ✅ Dispute mediation
- ✅ AI chat assistant with session management

### Upcoming Features (v1.1)
- 🔄 User authentication and authorization
- 🔄 Document version control
- 🔄 Collaborative features
- 🔄 Advanced analytics dashboard
- 🔄 Mobile application

### Future Plans (v2.0)
- 📋 Multi-language support
- 📋 Voice interface
- 📋 Integration with legal databases
- 📋 Automated document drafting
- 📋 Court filing assistance

---

**Built for Indian legal professionals**

*Last Updated: April 2026*
