#!/bin/bash
# Wait for PostgreSQL to start
until psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"

# Check if the required schema/table exists
SCHEMA_EXISTS=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'models_only_ogimet_stations');")

if [ "$SCHEMA_EXISTS" = 't' ]; then
    echo "Schema is ready. Proceeding with data migration..."
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /Ogimet_stations.sql
    echo "Data migration completed successfully."
else
    echo "Schema not ready. Data migration aborted."
fi
