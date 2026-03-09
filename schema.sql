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
