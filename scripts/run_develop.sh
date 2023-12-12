#!/bin/bash

echo "Generate migrations"
alembic revision --autogenerate -m "init" &


echo "Run migrations"
alembic upgrade head &

echo "Running server"
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000
