#!/bin/bash

# Kill all processes on port 8000
fuser -k 8000/tcp
sleep 1

# Start Redis
redis-server --daemonize yes

sleep 5

cd vlp
# Start Django

# Start Celery
celery -A server worker --loglevel=info &


gunicorn --bind 0.0.0.0:8000 server.wsgi:application

# Start Celery Beat if needed
# echo "Starting Celery Beat..."
celery -A server beat --loglevel=info &

echo "Django and Celery are running."

# Keep the shell open
wait