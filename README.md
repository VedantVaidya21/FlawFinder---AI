# FlawFinder AI Backend

A scalable, modular FastAPI backend for workflow flaw analysis and reporting.

## Features
- User authentication (JWT, signup/login)
- Upload workflow (CSV/JSON)
- Automated flaw analysis (mocked AI)
- Dashboard, fix plan, and executive report endpoints
- Modular: routers, models, services, utils
- PostgreSQL with SQLAlchemy async ORM

## Folder Structure
```
flawfinder-ai/
├── main.py
├── .env
├── requirements.txt
├── README.md
├── db/
│   └── session.py
├── models/
│   ├── user.py
│   ├── workflow.py
│   ├── flaw.py
│   ├── fix_suggestion.py
│   └── report.py
├── routers/
│   ├── auth.py
│   ├── upload.py
│   ├── analyze.py
│   ├── dashboard.py
│   ├── fix_plan.py
│   └── report.py
├── services/
├── utils/
│   ├── jwt_helper.py
│   ├── auth.py
│   └── response.py
```

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up PostgreSQL and update `.env` with credentials.
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
4. Access Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)

## Notes
- Uses async SQLAlchemy and FastAPI
- JWT-protected endpoints
- Replace dummy/mock logic with real AI and business logic as needed
