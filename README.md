# AI-Enhanced Incident Response System

An intelligent system for processing social care call/meeting transcripts, analyzing them against organizational policies, and automatically generating incident reports with appropriate email notifications.

## Overview

This prototype demonstrates an AI-powered workflow for social care incident management. The system ingests call transcripts (via text input or file upload), uses vector search to identify relevant policies, and leverages OpenAI's API to generate structured incident reports and draft professional email communications.

**Core Capabilities:**
- **Transcript Processing**: Accept text input or file uploads (.txt, .md)
- **Policy Matching**: Vector-based semantic search against pre-ingested policies using SQLite with sqlite-vec extension
- **Automated Report Generation**: Structured incident forms based on policy requirements
- **Email Drafting**: Context-aware email generation for supervisors, risk assessors, and family members
- **Reasoning Transparency**: Displays policy references and AI reasoning for fact-checking

## Architecture

### Backend (Python/FastAPI)

**Stack**: Python 3.12+, FastAPI, OpenAI Agents SDK, SQLite + sqlite-vec, aiosqlite

**Key Components:**
- **API Layer** ([main.py](backend/main.py), [processor.py](backend/app/api/v1/processor.py)):
  - `/api/v1/transcript` - Main endpoint accepting transcript text and/or file upload
  - Error handling with comprehensive logging
  - CORS enabled for local development (ports 5173, 3000)

- **Vector Search** ([db.py](backend/app/db/db.py), [vector_search.py](backend/ingestion/vector_search.py)):
  - SQLite database with sqlite-vec extension for embedding-based policy retrieval
  - OpenAI `text-embedding-3-small` model for vectorization
  - Deduplication logic using SHA-1 hashing of policy texts
  - Returns top-k (k=10) matching policies with distance scores

- **Agent System** ([processor.py](backend/app/api/v1/processor.py#L46-L50)):
  - OpenAI Agents SDK with structured output (`PolicyProcessingResults`)
  - Tool: `search_policies` - semantic search for relevant policies
  - Generates incident reports, emails, and reasoning chains

- **Data Ingestion** ([ingestion.py](backend/ingestion/ingestion.py)):
  - Processes policy documents from filesystem
  - Uses GPT-4o-mini to generate example situations for each policy
  - Creates embeddings and populates SQLite vector database

- **File Processing** ([file_processing.py](backend/app/utils/file_processing.py)):
  - Validates file type (.txt, .md), content-type, size (1MB limit)
  - UTF-8 encoding verification
  - Streaming validation to prevent memory exhaustion

**Data Models** ([schemas/](backend/app/schemas/)):
- `IncidentReport` - Structured incident form fields (datetime, location, type, actions, risk assessment)
- `Email` - To/CC/BCC, subject, markdown body
- `PolicyProcessingResults` - Combines report, emails, policy IDs, and reasoning
- `SituationSearchResult` - Vector search result with distance score

### Frontend (Next.js/React)

**Stack**: React 19, Vite, TypeScript, TailwindCSS, react-dropzone, react-markdown

**Key Components:**
- **App.tsx** ([App.tsx](frontend/src/App.tsx)): Main application orchestration
  - Form handling for text input and file upload
  - API integration via `@hey-api/openapi-ts` generated client
  - Auto-scroll to results after processing

- **FileUpload** ([FileUpload.tsx](frontend/src/components/FileUpload.tsx)):
  - Drag-and-drop interface with validation
  - Client-side file type/size checks
  - Real-time feedback on upload status

- **IncidentReportDisplay** ([IncidentReportDisplay.tsx](frontend/src/components/IncidentReportDisplay.tsx)):
  - Structured grid layout for all incident fields
  - Visual indicators for boolean fields (first aid, emergency services, risk assessment)

- **EmailsDisplay** ([EmailsDisplay.tsx](frontend/src/components/EmailsDisplay.tsx)):
  - Carousel navigation for multiple emails
  - Markdown rendering for email bodies
  - Displays To/CC/BCC recipients

- **PoliciesDisplay** ([PoliciesDisplay.tsx](frontend/src/components/PoliciesDisplay.tsx)):
  - Shows all referenced policies with markdown formatting
  - Visual separation for easy scanning

- **ReasoningDisplay** ([ReasoningDisplay.tsx](frontend/src/components/ReasoningDisplay.tsx)):
  - Numbered list of AI reasoning steps
  - Links specific transcript excerpts to policy sections for fact-checking

**API Type Generation:**
- Uses `@hey-api/openapi-ts` to generate TypeScript client from OpenAPI spec
- Command: `npm run generate:api`

## Getting Started

### Prerequisites
- Python 3.12+ with `uv` package manager
- Node.js 18+ with npm
- OpenAI API key

### Backend Setup

```bash
cd backend

# Create .env file with OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Install dependencies
uv sync

# (Optional) Ingest policies if database doesn't exist
# This reads policy files and populates the vector database
# Please see read me at `backend/ingestion/README.md` for details to get this working on MacOS
uv run ingestion/ingestion.py

# Run development server
uv run fastapi dev main.py
```

Backend runs on: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# (Optional) Generate API types from backend OpenAPI spec - note backend has to be running 
npm run generate:api

# Run development server
npm run dev
```

Frontend runs on: `http://localhost:5173`

## Usage

1. **Enter Transcript**: Paste transcript text or upload a .txt/.md file
2. **Analyze**: Click "Analyze Incident" to process
3. **Review Results**:
   - **Incident Report**: Structured form with all required fields
   - **Generated Emails**: Navigate through drafted emails for different recipients
   - **Policies Referenced**: Full text of matched policies
   - **Analysis Reasoning**: AI's explanation linking transcript to policies

4. **Fact-Checking**: Use reasoning section to verify AI outputs against policy text

## Bonus Features Status

### Implemented
✅ **Error Handling & Logging**: Comprehensive error handling throughout backend with structured logging
✅ **Fallback Mechanisms**: Graceful degradation when no policies found, file validation fallbacks
✅ **Fact-Checking Support**: Reasoning display shows policy quotes and transcript excerpts for verification

### Gap Analysis - Not Implemented

❌ **User Feedback Loop**: No mechanism for users to edit/refine AI-generated content with feedback
- **What's Missing**:
  - Edit interface for incident report fields
  - Regeneration endpoint that accepts corrections
  - Feedback collection for model fine-tuning
- **Implementation Effort**: Medium (2-3 days)
  - Add PATCH endpoint for report updates
  - Store feedback in database
  - Add edit UI with form validation
  - Implement regeneration with user context

## Innovative Enhancement Ideas

### 1. Email Provider Integration (High Impact, Medium Effort)
**Problem**: Users must manually copy email content to their email client
**Solution**: Direct integration with Gmail/Outlook APIs to draft emails in user's account
- OAuth2 authentication flow
- Gmail/Outlook API integration to create draft emails
- One-click "Send to Drafts" from UI
- **Technical Stack**: OAuth libraries, provider SDKs, backend session management
- **Value**: Reduces manual work, minimizes copy-paste errors, maintains email context

### 2. Emergency Service Auto-Dial with Human-in-Loop (Critical Impact, High Effort)
**Problem**: Time-critical incidents require manual emergency service contact
**Solution**: Automated emergency service notification with mandatory human approval
- Parse incident severity from transcript (falls with injury, medication errors, etc.)
- Generate pre-filled emergency call script
- Twilio/VoIP integration for automated or assisted calling
- **Safety Gates**:
  - Mandatory human approval before dialing
  - Incident severity threshold configuration
  - Audit log of all emergency calls
- **Technical Stack**: Twilio API, severity classification model, audit database
- **Value**: Faster emergency response, reduced human error in high-stress situations

### 3. Production Vector Database Migration (Scalability, Medium Effort)
**Problem**: SQLite + sqlite-vec suitable for prototype, not for production scale
**Solution**: Migrate to production-grade vector database
- **Options**:
  - **MongoDB Atlas Vector Search**: Native vector search with existing MongoDB infra, mature ecosystem
  - **Pinecone**: Managed vector DB, purpose-built for embeddings, excellent performance
  - **Weaviate**: Open-source, hybrid search (vector + keyword), GraphQL API
- **Migration Path**:
  - Abstract vector operations behind interface/repository pattern
  - Parallel running during migration for validation
  - Benchmark query performance (latency, accuracy)
- **Value**: Horizontal scaling, better query performance, production reliability, multi-tenancy support

**Recommendation Priority**: Emergency Auto-Dial > Email Integration > Vector DB Migration
(Rationale: Emergency auto-dial has highest impact on patient safety, core mission of social care)

## Technology Decisions

**Why SQLite + sqlite-vec?**
Rapid prototyping with zero infrastructure overhead. Single-file database with vector search capabilities sufficient for demo scale (<10k policies).

**Why OpenAI Agents SDK?**
Provides structured output parsing, tool integration, and multi-step reasoning out-of-the-box. Reduces boilerplate for agentic workflows.

**Why React + Vite?**
Fast development experience with HMR, TypeScript support, and minimal configuration. TailwindCSS for rapid UI development.

**Why FastAPI?**
Async-native Python framework with automatic OpenAPI generation, type validation via Pydantic, and excellent developer experience.

## Project Structure

```
askEmma/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── db/              # Database utilities
│   │   ├── schemas/         # Pydantic models
│   │   └── utils/           # Tools and file processing
│   ├── ingestion/           # Policy ingestion scripts
│   ├── db/                  # SQLite database file
│   ├── main.py              # FastAPI app entry
│   └── pyproject.toml       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── client/          # Generated API client
│   │   └── App.tsx          # Main app
│   └── package.json         # Node dependencies
└── the_task.md              # Original requirements
```

## License

Proprietary - AskEmma Take-Home Assignment
