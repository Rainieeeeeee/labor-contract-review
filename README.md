# AI Labor Contract Review — 劳动合同风险分析系统

An AI-powered tool that analyzes Chinese labor contracts for legal risks using RAG (Retrieval-Augmented Generation). Upload a contract, get a structured risk report with references to real labor law articles.

## Tech Stack

- **Backend:** Python, FastAPI
- **AI:** OpenAI `gpt-4o-mini` (analysis), `text-embedding-3-small` (embeddings)
- **Vector DB:** ChromaDB (semantic search over labor law articles)
- **Frontend:** React, Next.js, Tailwind CSS

## Features

- Upload a `.txt` labor contract and receive a clause-by-clause risk analysis
- Each risk finding is **grounded in real law articles** (防幻觉 RAG design)
- Risk levels: 高 / 中 / 低 — color-coded in the UI
- Automatic Swagger UI at `/docs` for API testing

## How It Works (RAG Pipeline)

```
Contract Upload
      │
      ▼
  Parse clauses          ← regex split by "第X条"
      │
      ▼
  Embed each clause      ← text-embedding-3-small
      │
      ▼
  Retrieve top-3 law articles  ← ChromaDB semantic search
      │
      ▼
  Analyze with LLM       ← gpt-4o-mini + law articles in prompt
      │
      ▼
  Structured JSON output  { risk_level, risk_description, suggestion }
```

The vector database is pre-built from 98 articles of 《中华人民共和国劳动合同法》(2012). RAG grounds every LLM response in real legal text, preventing hallucinated law citations.

## Project Structure

```
labor-contract-review/
├── scripts/
│   ├── parse_laws.py     # Parse law/contract text by article
│   ├── build_index.py    # Embed articles + store in ChromaDB
│   ├── retriever.py      # Clause → embedding → top-3 law search
│   ├── analyzer.py       # LLM risk analysis with law grounding
│   └── run_analysis.py   # End-to-end pipeline
├── app/api/routes.py     # FastAPI POST /analyze endpoint
├── main.py               # Server entry point
├── frontend/             # Next.js UI
└── data/laws/            # Labor law source text
```

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API key

### Backend

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Build the vector index (one-time setup)
cd scripts
python build_index.py

# Start the server
python main.py
# API running at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# UI running at http://localhost:3000
```

## API

```
POST /analyze
Content-Type: multipart/form-data

file: <contract .txt file>

Response: [
  {
    "risk_level": "高",
    "risk_description": "...",
    "violated_articles": ["第十九条"],
    "suggestion": "..."
  },
  ...
]
```
