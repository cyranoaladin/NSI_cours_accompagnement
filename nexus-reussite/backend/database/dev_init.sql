-- Nexus Réussite - Development Database Initialization
-- This script initializes the development database

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create basic indexes for better performance
-- (Tables will be created by Flask-Migrate/Alembic)

-- Set timezone
SET timezone = 'UTC';

-- Basic configuration
ALTER DATABASE nexus_dev SET timezone TO 'UTC';

-- Create demo user for testing (password will be hashed by the application)
-- This is just a placeholder - actual user creation happens through the API
