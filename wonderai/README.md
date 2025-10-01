# WonderAI - Modern AI Chatbot

**Goal:** A modern AI/ML-powered chatbot with React frontend and Python backend that can accept human prompts, incorporate them into its knowledge flow (RAG), and return rich responses including text, generated images, and embedded maps.

## Architecture

- **Frontend**: React 19 + Vite + Tailwind CSS + Shadcn/ui + Redux Toolkit
- **Backend**: FastAPI + SQLModel + PostgreSQL + Vector DB (FAISS/Pinecone)
- **AI**: OpenAI GPT-4/Hugging Face + Embeddings + Image Generation
- **Maps**: Leaflet/Mapbox GL JS for geolocation features
- **Deployment**: Docker + GitHub Actions + Cloud hosting

## Project Structure

```
wonderai/
├─ frontend/        # React + Vite + Tailwind + Shadcn/ui
├─ backend/         # FastAPI + SQLModel + Vector DB
├─ infra/           # Docker Compose, K8s manifests
├─ .github/         # CI/CD workflows
└─ README.md
```

## Core Features

1. **Conversational UI** - Modern chat interface with streaming responses
2. **RAG Knowledge System** - Real-time learning from conversations
3. **Image Generation** - AI-powered image creation in responses
4. **Map Integration** - Embedded maps with markers and routes
5. **Real-time Updates** - WebSocket/SSE streaming
6. **Performance Optimized** - React.memo, memoization, code splitting

## Getting Started

### Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- Docker and Docker Compose
- OpenAI API key (or Hugging Face)

### Development Setup

1. **Clone and setup**:
```bash
git clone <repo-url>
cd wonderai
```

2. **Frontend setup**:
```bash
cd frontend
npm install
npm run dev
```

3. **Backend setup**:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

4. **Full stack with Docker**:
```bash
docker-compose up --build
```

## API Endpoints

- `POST /api/chat` - Send message and get AI response
- `POST /api/chat/stream` - WebSocket streaming chat
- `POST /api/generate-image` - Generate images from text
- `GET /api/maps/metadata` - Geocoding and map helpers

## Environment Variables

```bash
# Backend
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:pass@localhost/wonderai
VECTOR_DB_URL=your_vector_db_connection

# Frontend
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

## Development

- Frontend runs on `http://localhost:5173`
- Backend runs on `http://localhost:8000`
- API docs available at `http://localhost:8000/docs`

## Deployment

Uses GitHub Actions for CI/CD:
- Frontend → Vercel/Netlify
- Backend → Railway/Render/AWS ECS
- Database → PostgreSQL cloud service
- Vector DB → Pinecone/Weaviate managed service

## Tech Stack Details

### Frontend
- **React 19** with concurrent features and Suspense
- **Vite** for fast development and optimized builds
- **Tailwind CSS** utility-first styling
- **Shadcn/ui** for all UI components
- **Redux Toolkit** for state management
- **Axios** for HTTP requests
- **React Query** for data fetching and caching
- **Leaflet** for interactive maps

### Backend
- **FastAPI** for high-performance API
- **SQLModel** for type-safe database operations
- **PostgreSQL** for relational data
- **FAISS/Pinecone** for vector similarity search
- **OpenAI/Hugging Face** for LLM integration
- **Stable Diffusion** for image generation
- **WebSockets** for real-time communication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the coding standards (SOLID principles, React best practices)
4. Add tests for new features
5. Submit a pull request

## License

MIT License - see LICENSE file for details
