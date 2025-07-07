#!/bin/bash
/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "PostgreSQL is up"

python manage.py migrate

if [ -f "/app/theatre_dump.json" ]; then
  echo "Loading fixture theatre_dump.json"
  python manage.py loaddata /app/theatre_dump.json
fi

python manage.py runserver 0.0.0.0:8000