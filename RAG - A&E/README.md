# AI Triage RAG Agent

A safe, local AI assistant that asks patients structured questions, spots red flags, and suggests urgency bands for clinicians, using a RAG system that pulls from trusted medical guidance.

## Overview

This system is designed for A&E and urgent care settings to:
- Collect structured symptom information from patients before or at arrival
- Flag obvious red-flag situations and suggest urgency bands (Red/Amber/Green)
- Show clinicians a summary page of answers + red flags
- Run locally (or on-prem server) so no patient data leaves the Trust

## Project Structure

```
.
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── core/    # Triage engine, logging, config
│   │   ├── models/  # Pydantic models
│   │   └── routers/ # API endpoints
│   └── requirements.txt
├── frontend/         # React TypeScript frontend
│   └── src/
│       ├── components/
│       └── types.ts
└── docker-compose.yml
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OR Python 3.11+ and Node.js 18+ for local development

### Using Docker (Recommended)

1. Clone/navigate to the project directory
2. Start all services:
   ```bash
   docker-compose up
   ```
3. Access:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### POST /api/triage

Assess patient triage and return urgency band.

**Request:**
```json
{
  "age": 45,
  "sex": "M",
  "chief_complaint": "chest_pain",
  "answers": {
    "shortness_of_breath": true,
    "sweating": true,
    "heart_disease": true
  }
}
```

**Response:**
```json
{
  "urgency": "red",
  "red_flags": [
    {
      "flag": "Chest pain with shortness of breath",
      "severity": "red"
    },
    {
      "flag": "Chest pain with history of heart disease",
      "severity": "red"
    }
  ],
  "explanation": "RED: chest pain with red flags: Chest pain with shortness of breath, Chest pain with history of heart disease. Requires immediate clinical assessment.",
  "assessed_at": "2024-01-01T12:00:00",
  "model_version": "rule-based-v1.0",
  "rule_version": "v1.0"
}
```

### GET /api/health

Health check endpoint.

## Supported Chief Complaints

- `chest_pain`
- `shortness_of_breath`
- `abdominal_pain`
- `headache`
- `fever_infection`
- `injury`

## Urgency Bands

- **RED**: Needs immediate clinician assessment
- **AMBER**: Urgent but not life-threatening
- **GREEN**: Low risk / could be redirected

## Safety Features

- Rule-based red flag detection (deterministic, safest)
- Conservative fallback: if assessment fails, defaults to higher urgency
- All requests logged for audit trail
- Version tracking for model and rules

## Next Steps (Future Enhancements)

- [ ] Add RAG component with vector database
- [ ] Clinician dashboard for reviewing triage entries
- [ ] Database integration (PostgreSQL + pgvector)
- [ ] Local LLM integration (Ollama/llama.cpp)
- [ ] Integration with Trust systems

## Development Status

**Current:** Step 1 & 2 Complete
- ✅ Backend triage logic & API
- ✅ Simple frontend for patient form
- ⏳ RAG component (Step 3)
- ⏳ Clinician dashboard (Step 4)

## License

This is a prototype system for demonstration purposes. Not for clinical use without proper validation and regulatory approval.


