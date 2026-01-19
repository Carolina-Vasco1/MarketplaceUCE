DO
$$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'blockchain_db') THEN
    CREATE DATABASE blockchain_db;
  END IF;
END
$$;

DO
$$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'blockchain') THEN
    CREATE USER blockchain WITH PASSWORD 'blockchain';
  END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE blockchain_db TO blockchain;
