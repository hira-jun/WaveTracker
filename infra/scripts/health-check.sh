#!/usr/bin/env sh
set -eu

echo "Checking backend..."
curl -fsS http://localhost:8000/health >/dev/null
echo "Checking frontend..."
curl -fsS http://localhost:3000 >/dev/null
echo "Checking postgres port..."
nc -z localhost 5432
echo "All services are reachable."
