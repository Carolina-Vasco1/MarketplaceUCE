
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'blockchain') THEN
      CREATE ROLE blockchain LOGIN PASSWORD 'blockchain';
   END IF;
END
$$;

DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'blockchain_db') THEN
      CREATE DATABASE blockchain_db OWNER blockchain;
   END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE blockchain_db TO blockchain;
