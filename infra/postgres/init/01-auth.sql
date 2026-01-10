CREATE DATABASE auth_db;

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'auth') THEN
    CREATE ROLE auth LOGIN PASSWORD 'auth';
  END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE auth_db TO auth;

\c auth_db

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'buyer',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO auth;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO auth;

-- admin inicial (password: admin123)
INSERT INTO users (email, password_hash, role)
VALUES (
  'admin@uce.edu.ec',
  '$2b$12$kIXQJQvZk9uJ2PqYFfFz9O2Yw9L9KQpYh5FjYtZ9OQ0zZqQ0ZqQ0Z',
  'admin'
)
ON CONFLICT (email) DO NOTHING;
