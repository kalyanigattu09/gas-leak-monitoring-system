-- PostgreSQL setup for Smart Gas Monitoring System
-- Run as a PostgreSQL superuser (e.g. postgres)

-- Create database
CREATE DATABASE smart_gas_db
    WITH
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TEMPLATE = template0;

-- Optional: create a dedicated application user
-- CREATE USER smart_gas_user WITH PASSWORD 'your_secure_password';
-- GRANT ALL PRIVILEGES ON DATABASE smart_gas_db TO smart_gas_user;
-- \c smart_gas_db
-- GRANT ALL ON SCHEMA public TO smart_gas_user;
