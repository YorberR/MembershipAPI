-- Initialize the database
CREATE DATABASE fastapi_db;

-- Create user if not exists
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'fastapi_user') THEN

      CREATE ROLE fastapi_user LOGIN PASSWORD 'fastapi_password';
   END IF;
END
$do$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;