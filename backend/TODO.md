# TODO for PostgreSQL Migration

- [x] 1) BACKUP & GIT
  - Create git branch: db/postgres-migration
  - Backup backend/app.db to backend/backups/app.db.bak
  - Backup backend/app/integrations to backend/backups/integrations_backup

- [x] 2) SEARCH & REPORT
  - List files referencing Neo4j or SQLite (done)
  - Identify files to edit vs remove

- [x] 3) REMOVE / UNWIND DEPENDENCIES
  - Edit backend/requirements.txt to remove Neo4j and SQLite packages
  - Add psycopg2-binary, SQLAlchemy, alembic
  - Provide pip uninstall commands for Neo4j drivers

- [x] 4) ENVIRONMENT
  - Replace backend/.env with PostgreSQL config only
  - Create backend/.env.example with placeholders

- [x] 5) DB MODULE
  - Confirm backend/app/db.py as canonical
  - Patch model files to import Base from app.db
  - Update alembic/env.py to use app.db.Base and DATABASE_URL

- [ ] 6) MIGRATIONS
  - Provide commands to create and run initial migration

- [ ] 7) OPTIONAL DATA MIGRATION
  - Provide optional Neo4j to Postgres migration script
  - Provide optional SQLite to Postgres migration instructions

- [ ] 8) GRAPH REPO
  - Provide SQL-based graph repo and NetworkX analysis replacements

- [ ] 9) SCRIPTS + TESTS + DOCS
  - Create backend/scripts/setup_postgres.sql
  - Create backend/tests/test_db_connection.py
  - Create backend/SETUP_POSTGRES.md
  - Add Makefile targets for db-setup, migrate, test-conn

- [x] 10) REMOVE FILES SAFELY
  - Backup commands for app.db and Neo4j integration folder
  - Provide commented removal commands

- [x] 11) SANITY CHECK / CI
  - Add /ping-db route in app/main.py
  - Suggest unit tests for graph logic comparison
