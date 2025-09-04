-- FlawFinder AI Database Setup Script
-- PostgreSQL Database Schema Creation

-- Create database and user
CREATE DATABASE flawfinder_db;
CREATE USER flawfinder WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE flawfinder_db TO flawfinder;

-- Connect to the database
\c flawfinder_db;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO flawfinder;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flawfinder;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO flawfinder;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create organizations table
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    industry VARCHAR(100),
    size VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'analyst' CHECK (role IN ('admin', 'analyst', 'engineer', 'exec')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    organization_id INTEGER REFERENCES organizations(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create process_flows table
CREATE TABLE process_flows (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    raw_input TEXT NOT NULL,
    parsed_graph JSONB,
    version INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'processing', 'completed', 'failed')),
    brutality_score FLOAT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    organization_id INTEGER REFERENCES organizations(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create findings table
CREATE TABLE findings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    finding_type VARCHAR(50) NOT NULL CHECK (finding_type IN ('bottleneck', 'redundancy', 'manual_handoff', 'wait_time', 'rework_loop', 'data_duplication', 'inefficient_process')),
    impact_score FLOAT NOT NULL CHECK (impact_score >= 0 AND impact_score <= 100),
    node_id VARCHAR(100),
    tags JSONB,
    recommendations JSONB,
    process_flow_id INTEGER NOT NULL REFERENCES process_flows(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create brutality_scores table
CREATE TABLE brutality_scores (
    id SERIAL PRIMARY KEY,
    score FLOAT NOT NULL CHECK (score >= 0 AND score <= 100),
    breakdown JSONB,
    version VARCHAR(50),
    process_flow_id INTEGER NOT NULL REFERENCES process_flows(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create reports table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    report_type VARCHAR(30) NOT NULL CHECK (report_type IN ('ceo_report', 'department_report', 'technical_report')),
    status VARCHAR(20) DEFAULT 'generating' CHECK (status IN ('generating', 'completed', 'failed')),
    content JSONB,
    file_url VARCHAR(500),
    report_metadata JSONB,
    user_id INTEGER NOT NULL REFERENCES users(id),
    process_flow_id INTEGER REFERENCES process_flows(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task_type VARCHAR(30) NOT NULL CHECK (task_type IN ('flow_parsing', 'score_calculation', 'report_generation', 'model_training', 'data_drift_monitoring')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    progress FLOAT DEFAULT 0.0 CHECK (progress >= 0 AND progress <= 100),
    result JSONB,
    error_message TEXT,
    logs JSONB,
    task_metadata JSONB,
    user_id INTEGER NOT NULL REFERENCES users(id),
    process_flow_id INTEGER REFERENCES process_flows(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create ml_pipelines table
CREATE TABLE ml_pipelines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    model_path VARCHAR(500),
    metrics_endpoint VARCHAR(500),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'error')),
    pipeline_metadata JSONB,
    user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create drift_metrics table
CREATE TABLE drift_metrics (
    id SERIAL PRIMARY KEY,
    drift_type VARCHAR(20) NOT NULL CHECK (drift_type IN ('data_drift', 'concept_drift', 'label_drift')),
    metric_value FLOAT NOT NULL,
    threshold FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    drift_metadata JSONB,
    pipeline_id INTEGER NOT NULL REFERENCES ml_pipelines(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create retraining_events table
CREATE TABLE retraining_events (
    id SERIAL PRIMARY KEY,
    trigger_reason VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    model_version VARCHAR(100),
    performance_metrics JSONB,
    retraining_metadata JSONB,
    pipeline_id INTEGER NOT NULL REFERENCES ml_pipelines(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_organization_id ON users(organization_id);
CREATE INDEX idx_process_flows_user_id ON process_flows(user_id);
CREATE INDEX idx_process_flows_organization_id ON process_flows(organization_id);
CREATE INDEX idx_process_flows_status ON process_flows(status);
CREATE INDEX idx_findings_process_flow_id ON findings(process_flow_id);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_brutality_scores_process_flow_id ON brutality_scores(process_flow_id);
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_process_flow_id ON reports(process_flow_id);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_ml_pipelines_user_id ON ml_pipelines(user_id);
CREATE INDEX idx_drift_metrics_pipeline_id ON drift_metrics(pipeline_id);
CREATE INDEX idx_retraining_events_pipeline_id ON retraining_events(pipeline_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_process_flows_updated_at BEFORE UPDATE ON process_flows FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_findings_updated_at BEFORE UPDATE ON findings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_brutality_scores_updated_at BEFORE UPDATE ON brutality_scores FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reports_updated_at BEFORE UPDATE ON reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ml_pipelines_updated_at BEFORE UPDATE ON ml_pipelines FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_drift_metrics_updated_at BEFORE UPDATE ON drift_metrics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_retraining_events_updated_at BEFORE UPDATE ON retraining_events FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO organizations (name, description, industry, size) VALUES
('Acme Corp', 'A leading technology company', 'Technology', 'large'),
('StartupXYZ', 'Innovative startup in fintech', 'Financial Services', 'small'),
('Enterprise Inc', 'Large enterprise with complex processes', 'Manufacturing', 'enterprise');

-- Insert sample admin user (password: admin123 - hashed with bcrypt)
INSERT INTO users (email, hashed_password, first_name, last_name, role, organization_id) VALUES
('admin@flawfinder.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9Kz8K2O', 'Admin', 'User', 'admin', 1),
('analyst@acme.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9Kz8K2O', 'John', 'Analyst', 'analyst', 1),
('engineer@startup.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/9Kz8K2O', 'Jane', 'Engineer', 'engineer', 2);

-- Grant all privileges to the flawfinder user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flawfinder;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO flawfinder;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO flawfinder;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO flawfinder;

COMMIT;
