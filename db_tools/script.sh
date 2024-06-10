#!/bin/bash
# Wait for the backend to initialize the schema
sleep 60

# Check if the required schema/table exists
SCHEMA_EXISTS=$(psql -U admin -d firma -Atc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'models_only_ogimet_stations');")

if [ "$SCHEMA_EXISTS" = 't' ]; then
    echo "Schema is ready. Proceeding with data migration..."
    # Copy data file to container - assuming the file is already in a mounted volume
    psql -U admin -d firma -f /file.sql
    echo "done"
else
    echo "Schema not ready. Data migration aborted."
fi
