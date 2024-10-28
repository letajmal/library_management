#!/bin/bash

# Initialize the database
echo "Initializing database..."
flask init-db

# Start the application
echo "Starting application..."
exec flask run --host=0.0.0.0 --port=$PORT