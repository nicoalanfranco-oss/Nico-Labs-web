-- Database Schema for Nico Labs Web
-- This script creates the tables required for lead capture and chatbot persistent memory.

-- Table for Contact Leads
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    domicilio TEXT,
    project_interest TEXT,
    source VARCHAR(50) DEFAULT 'web_contact_form',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for Chat Sessions / Memory
-- Used by n8n Postgres Chat Memory node
CREATE TABLE IF NOT EXISTS chat_memory (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    message_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster session lookups
CREATE INDEX IF NOT EXISTS idx_chat_memory_session ON chat_memory(session_id);

-- --- Row Level Security (RLS) Policies ---
-- Since insertions and queries are performed via n8n/webhook using a dedicated database role:

-- 1. Enable RLS on tables
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_memory ENABLE ROW LEVEL SECURITY;

-- 2. Define policies for 'leads'
-- The web interface does NOT access PostgreSQL directly; insertions and queries are done via n8n.
-- We grant full access (SELECT, INSERT, UPDATE, DELETE) only to authorized database roles (e.g. admin or the role used by n8n).
CREATE POLICY webhook_role_all_access_leads ON leads
    FOR ALL
    USING (current_user = 'nlanfranco' OR current_user = 'admin' OR current_user = 'n8n_user')
    WITH CHECK (current_user = 'nlanfranco' OR current_user = 'admin' OR current_user = 'n8n_user');

-- 3. Define policies for 'chat_memory'
-- Full CRUD permissions for n8n/webhook roles to manage chatbot memory.
CREATE POLICY webhook_role_all_access_memory ON chat_memory
    FOR ALL
    USING (current_user = 'nlanfranco' OR current_user = 'admin' OR current_user = 'n8n_user')
    WITH CHECK (current_user = 'nlanfranco' OR current_user = 'admin' OR current_user = 'n8n_user');

