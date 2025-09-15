# Backend Refactor: Remove PostgreSQL and SQLAlchemy, Integrate Neo4j

## Overview
Refactor the entire `flawfinder-ai` backend to use Neo4j as the only database, removing all PostgreSQL and SQLAlchemy references.

## Steps

### 1. Remove PostgreSQL and SQLAlchemy Files
- [ ] Delete `backend/migrations/` folder and all migration scripts
- [ ] Remove SQLAlchemy models: `user.py`, `report.py`, `process_flow.py`, `organization.py`, `finding.py`, `brutality_score.py`, `task.py`, `token.py`, `agentops.py`
- [ ] Remove PostgreSQL-related config from `env.example` and `config.py`

### 2. Ensure Neo4j Database Integration
- [ ] Verify `app/core/database.py` provides Neo4j async driver and session management
- [ ] Ensure `main.py` connects/disconnects from Neo4j on startup/shutdown
- [ ] Fix any circular imports or issues in database.py

### 3. Refactor Backend Logic to Neo4j
- [ ] Update all API routes to use Neo4j async sessions and Cypher queries
- [ ] Replace CRUD operations with Cypher queries
- [ ] Replace joins/relations with graph relationships
- [ ] Use Neo4j Pydantic models for data representation

### 4. Fix Imports and Dependencies
- [ ] Update all imports to use Neo4j models (`user_neo4j`, `report_neo4j`, etc.)
- [ ] Ensure imports from `app.core.database import db`
- [ ] Remove any broken or unused imports

### 5. Final Cleanup and Testing
- [ ] Verify no SQLAlchemy or alembic references remain
- [ ] Ensure exception handlers, routers, and models are compatible with Neo4j
- [ ] Run backend tests to verify functionality
- [ ] Remove SQLAlchemy and alembic dependencies from requirements
- [ ] Confirm API schemas unchanged and frontend compatibility

## Progress Tracking
- [x] Plan created and approved
- [ ] Step 1: Remove PostgreSQL files
- [ ] Step 2: Verify Neo4j integration
- [ ] Step 3: Refactor backend logic
- [ ] Step 4: Fix imports
- [ ] Step 5: Final cleanup and testing
