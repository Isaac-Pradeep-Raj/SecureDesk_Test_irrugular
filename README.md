# SecureDesk_v2

SecureDesk_v2 is a local-first enterprise knowledge assistant with a React frontend and Flask backend.

## Stack
- Frontend: React + Vite + Tailwind
- Backend: Flask + JWT + SQLite
- Retrieval: FAISS + sentence-transformers (local)

## Repository Layout
- `frontend/` React client
- `backend/` Flask API and services

## Quick Start
1. Backend
   - `cd backend`
   - `python -m venv venv`
   - `venv\\Scripts\\activate`
   - `pip install -r requirements.txt`
   - `copy .env.example .env`
   - `python app.py`
2. Frontend
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## Environment
Backend environment variables are defined in `backend/.env.example`.

## GitHub Push (first time)
1. `git init`
2. `git add .`
3. `git commit -m "Initial commit"`
4. `git branch -M main`
5. `git remote add origin https://github.com/Isaac-Pradeep-Raj/SecureDesk_V2.git`
6. `git push -u origin main`