PROJECT NAME

SecureDesk V2 — Secure Role-Aware Enterprise Knowledge Assistant Using Local RAG

PROJECT PURPOSE

SecureDesk is an enterprise knowledge assistant designed to allow employees to query internal organizational documents through a conversational interface while maintaining governance, privacy, and domain ownership awareness.

The system is NOT a generic chatbot.

It is a:

Privacy-preserving, context-aware enterprise knowledge system with controlled information governance and escalation workflows.

All enterprise data must remain local and never leave organizational infrastructure.

CORE PROBLEM BEING SOLVED

Organizations struggle with:

Scattered internal documentation

Dependency on HR/IT for repetitive queries

Ineffective keyword search

Confidentiality requirements

Unsafe external AI tools

SecureDesk creates a secure conversational layer over internal documents.

HIGH-LEVEL DESIGN PRINCIPLES

Local-first AI (no external data leakage)

Context-aware conversations

Domain ownership awareness

Practical enterprise governance

Human escalation when required

Lightweight deployment (solo developer friendly)

Industry-ready architecture

SYSTEM ARCHITECTURE OVERVIEW
React Frontend (Vite + Tailwind)
        ↓
Flask REST API
        ↓
Authentication + Governance Layer
        ↓
Document Processing Pipeline
        ↓
Vector Database (FAISS)
        ↓
Local RAG Retrieval
        ↓
Deterministic Response + Escalation Logic
TECH STACK (LOCKED)
Frontend

React (Vite)

TailwindCSS

Local state routing (no React Router yet)

JWT stored in localStorage

Backend

Python 3.11 (venv)

Flask

Flask-JWT-Extended

Flask-CORS

SQLite database

AI Stack

sentence-transformers (all-MiniLM-L6-v2)

FAISS (CPU)

spaCy (en_core_web_sm)

PyMuPDF (PDF extraction)

Environment Constraints

Target machine:

Ryzen 3 CPU

8GB RAM

CPU inference only

No heavy LLMs

AUTHENTICATION MODEL

JWT-based authentication.

Roles include:

HR

DEV

IT

Security

SuperAdmin

Role is embedded inside JWT token.

Frontend session persists using localStorage.

GOVERNANCE MODEL (VERY IMPORTANT)

SecureDesk DOES NOT block questions.

Users may ask anything.

Access control applies to information visibility, not queries.

Information Classification Levels
Classification	Meaning
PUBLIC	Visible to everyone
INTERNAL	Employees
RESTRICTED	Partial info + escalation
CONFIDENTIAL	Hidden, escalation required
Domain Ownership

Domains represent knowledge owners:

HR

DEV

IT

Security

Domain ≠ permission boundary.

Domain determines:

expertise owner

escalation contact

ESCALATION INTELLIGENCE (CORE FEATURE)

If:

information restricted

confidential data requested

confidence low

user requests confirmation

System provides escalation contact:

Department Owner
Email
Phone/Extension

No hard denial unless confidential.

FRONTEND STRUCTURE
src/
 ├── layout/
 │   ├── MainLayout.jsx
 │   ├── Sidebar.jsx
 │   └── Topbar.jsx
 │
 ├── pages/
 │   ├── LoginPage.jsx
 │   ├── ChatPage.jsx
 │   └── UploadPage.jsx
FRONTEND STATE MODEL

Global states in App.jsx:

role (authentication)

department (conversation context)

page ("chat" | "upload")

Sidebar controls:

navigation

domain context

CHAT SYSTEM BEHAVIOR

Chat request sends:

{
  "query": "...",
  "department": "IT"
}

Headers include:

Authorization: Bearer <JWT>

Backend returns:

{
  "answer": "...",
  "classification": "...",
  "escalation": {...}
}

Chat UI renders:

message bubbles

classification badge

escalation card

DOCUMENT INGESTION SYSTEM

Admins upload PDFs.

Upload flow:

UploadPage → /api/docs/upload
            ↓
Local storage (/uploads)
            ↓
SQLite metadata saved

Metadata stored:

filename

domain

classification

uploaded_by

Files NEVER leave server.

UPCOMING PIPELINE (NEXT DEVELOPMENT STAGE)

Document Processing:

Extract text (PyMuPDF)

Clean text

Chunk segmentation

Generate embeddings

Store vectors in FAISS

RAG Retrieval:

Query → Embed → Similarity Search → Context → Response
CONVERSATION CONTEXT MODEL

Each session tracks:

active department

role

conversation continuity

Sidebar selection updates domain context.

SECURITY PRINCIPLES

No external AI APIs for document data

Local embeddings only

JWT protected APIs

Governance-aware responses

Escalation instead of exposure

CURRENT PROJECT STATUS

Implemented:

✅ Authentication system
✅ Role-aware UI
✅ Context-aware chat
✅ Escalation framework
✅ Enterprise dashboard layout

Next:
➡ Document upload system
➡ Document processing pipeline
➡ Embedding generation
➡ FAISS retrieval integration

DEVELOPMENT CONSTRAINTS

Solo developer

Rapid iteration

Maintain readability over micro-optimization

Prefer simple modular Flask patterns

Avoid heavy frameworks

EXPECTED ASSISTANT BEHAVIOR (FOR CODEX)

When generating code:

Maintain existing architecture.

Prefer minimal dependencies.

Keep logic modular.

Respect governance model.

Never introduce cloud data transfer.

Assume local deployment.

Preserve role + domain + classification logic.

PROJECT GOAL

SecureDesk should evolve into:

A deployable enterprise knowledge copilot suitable for IT consulting environments and enterprise onboarding systems.

✅ END OF INITIALIZATION