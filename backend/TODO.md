# PostgreSQL/SQLAlchemy Cleanup Tasks

## Files to Remove
- [x] backend/alembic.ini (file not found - already removed)
- [x] backend/migrations/ (directory not found - already removed)
- [x] database_setup.sql (file not found - already removed)
- [x] setup_database.py (file not found - already removed)

## Files to Update
- [x] backend/app/core/database.py - Converted to Neo4j
- [x] backend/app/db.py - Already converted to Neo4j
- [x] backend/app/models/base.py - Already converted to Pydantic
- [ ] backend/app/models/user.py - Check for SQLAlchemy imports
- [ ] backend/app/models/organization.py - Check for SQLAlchemy imports
- [ ] backend/app/models/report.py - Check for SQLAlchemy imports
- [ ] backend/app/models/task.py - Check for SQLAlchemy imports
- [ ] backend/app/models/process_flow.py - Check for SQLAlchemy imports
- [ ] backend/app/models/finding.py - Check for SQLAlchemy imports
- [ ] backend/app/models/brutality_score.py - Check for SQLAlchemy imports
- [ ] backend/app/models/agentops.py - Check for SQLAlchemy imports
- [ ] backend/app/api/auth.py - Check for SQLAlchemy dependencies
- [ ] backend/app/api/flows.py - Check for SQLAlchemy dependencies
- [ ] backend/app/api/reports.py - Check for SQLAlchemy dependencies
- [ ] backend/app/api/agentops.py - Check for SQLAlchemy dependencies
- [ ] backend/app/core/config.py - Check for PostgreSQL DATABASE_URL
- [x] backend/requirements.txt - SQLAlchemy dependencies already removed
- [x] backend/docker-compose.yml - Already uses Neo4j, no PostgreSQL service

## Files to Create
- [x] backend/app/core/neo4j.py - Neo4j connection utility already exists
- [x] backend/app/models/ - Models already converted to Pydantic
- [ ] backend/app/services/ - Check if service classes exist for Neo4j operations

## Verification
- [ ] Ensure all imports are updated
- [ ] Test that the application can start without errors
- [ ] Verify that no PostgreSQL/SQLAlchemy references remain
