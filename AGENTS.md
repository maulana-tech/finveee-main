# AGENTS.md - MiroFish Development Guide

## Quick Start

```bash
# Copy and configure environment
cp .env.example .env

# Install all dependencies (root + frontend + backend)
npm run setup:all

# Start both frontend and backend
npm run dev
```

- Frontend: http://localhost:3000 (Vue 3 + Vite)
- Backend: http://localhost:5001 (Flask)

## Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start both frontend and backend |
| `npm run backend` | Start backend only |
| `npm run frontend` | Start frontend only |
| `npm run build` | Build frontend for production |

## Required Environment Variables

```env
LLM_API_KEY=your_key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus
ZEP_API_KEY=your_zep_key
```

## Architecture

- **Backend**: Flask app in `backend/app/`, entry point `backend/run.py`
- **Frontend**: Vue 3 in `frontend/src/`, built with Vite
- **Simulation**: Uses camel-ai (OASIS) library for agent-based social simulation

## Testing

```bash
cd backend && uv run pytest
```

## Notes

- Python 3.11-3.12 required (managed via uv)
- Backend uses `uv sync` for dependencies (see `backend/pyproject.toml`)
- LLM consumption is high; test with fewer than 40 simulation rounds first