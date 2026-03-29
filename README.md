# LegalGrid - Smart Legal System

A RAG-powered legal AI system for Indian law analysis, featuring contract analysis, case law retrieval, compliance monitoring, and dispute mediation.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ with `uv` installed
- Node.js 18+ with `pnpm` installed
- Docker (for Qdrant vector database)
- GROQ API key (free from https://console.groq.com)

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd LegalGrid
```

### 2. Backend Setup

```bash
cd backend

# Activate virtual environment (already created with uv)
source .venv/bin/activate

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start Qdrant vector database
docker-compose up -d

# Initialize database and seed sample data
python scripts/seed_data.py

# Start backend server
python main.py
```

Backend will be available at http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

Frontend will be available at http://localhost:5173

## 📚 Documentation

- [Executive Summary](EXECUTIVE_SUMMARY.md) - Project overview and quick reference
- [Roadmap](SMART_LEGAL_SYSTEM_ROADMAP.md) - 16-week development timeline
- [RAG Implementation](RAG_IMPLEMENTATION_GUIDE.md) - Technical deep dive
- [Data Sources](INDIAN_LEGAL_DATA_SOURCES.md) - Indian legal data sources
- [Quick Setup](QUICKSTART_SETUP.md) - Detailed setup instructions

## 🏗️ Architecture

```
┌─────────────┐
│   React     │  Frontend (Vite + TailwindCSS)
│  Frontend   │
└──────┬──────┘
       │ HTTP/REST
┌──────▼──────┐
│   FastAPI   │  Backend (Python)
│   Backend   │
└──────┬──────┘
       │
   ┌───┴────┬─────────┬──────────┐
   │        │         │          │
┌──▼──┐ ┌──▼───┐ ┌───▼────┐ ┌──▼────┐
│GROQ │ │Qdrant│ │LangChain│ │Agents│
│ LLM │ │Vector│ │  RAG   │ │ (4)  │
└─────┘ └──────┘ └────────┘ └──────┘
```

## 🎯 Features

### ✅ Implemented

- **Contract Analysis**: Upload contracts (PDF/TXT) and get risk analysis with red flags and recommendations
- **RAG Retrieval**: Hybrid semantic + BM25 search over Indian legal documents
- **Vector Database**: Qdrant integration with document collections
- **API Documentation**: Auto-generated Swagger UI at `/docs`

### 🚧 Coming Soon

- **Case Law Search**: Find relevant precedents from SC/HC
- **Compliance Monitoring**: Check regulatory compliance gaps
- **Dispute Mediation**: AI-powered multi-party mediation

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **LLM**: GROQ (openai/gpt-oss-120b)
- **Vector DB**: Qdrant
- **Embeddings**: sentence-transformers (all-mpnet-base-v2)
- **Agents**: LangChain
- **Package Manager**: uv

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite 8
- **Routing**: React Router 7
- **Styling**: TailwindCSS 4
- **HTTP Client**: Axios
- **Package Manager**: pnpm

## 📁 Project Structure

```
LegalGrid/
├── backend/
│   ├── app/
│   │   ├── agents/          # AI agents (contract, case, compliance, mediation)
│   │   ├── api/routes/      # API endpoints
│   │   ├── core/            # Config and LLM client
│   │   ├── models/          # Pydantic schemas
│   │   └── rag/             # RAG retrieval system
│   ├── scripts/             # Utility scripts
│   ├── main.py              # FastAPI app
│   └── docker-compose.yml   # Qdrant service
├── frontend/
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   └── App.jsx          # Main app
│   └── package.json
├── docs/                    # Documentation markdown files
└── README.md
```

## 🧪 Testing

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
pnpm test
```

## 🚀 Deployment

### Backend

```bash
# Using Docker
docker build -t legalgrid-backend .
docker run -p 8000:8000 legalgrid-backend

# Or deploy to Railway/Render
# See backend/README.md for details
```

### Frontend

```bash
cd frontend
pnpm build

# Deploy to Vercel
vercel

# Or upload dist/ to any static hosting
```

## 📊 API Endpoints

### Core
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Swagger UI

### Qdrant
- `POST /api/v1/qdrant/initialize` - Initialize collections
- `POST /api/v1/qdrant/add-document` - Add document
- `POST /api/v1/qdrant/search` - Search documents

### Contracts
- `POST /api/v1/contracts/analyze` - Analyze contract text
- `POST /api/v1/contracts/analyze-file` - Analyze uploaded file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Indian Kanoon for legal data
- GROQ for fast LLM inference
- Qdrant for vector database
- LangChain for agent framework

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ for Indian legal professionals
