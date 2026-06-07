-- PostgreSQL setup for Smart Gas Monitoring System (portable)
-- Run as a PostgreSQL superuser, e.g.:
--   psql -U postgres -f scripts/create_db_portable.sql

SELECT 'CREATE DATABASE smart_gas_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'smart_gas_db')\gexec

-- Optional dedicated application user (uncomment and set a strong password):
-- DO $$
-- BEGIN
--     IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'smart_gas_user') THEN
--         CREATE USER smart_gas_user WITH PASSWORD 'your_secure_password';
--     END IF;
-- END
-- $$;
-- GRANT ALL PRIVILEGES ON DATABASE smart_gas_db TO smart_gas_user;
