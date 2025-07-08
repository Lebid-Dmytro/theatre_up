#!/bin/bash
/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "PostgreSQL is up"

python manage.py migrate

if [ -f "initial_data.json" ]; then
  echo "Loading fixture initial_data.json"
  python manage.py loaddata initial_data.json
fi

python manage.py runserver 0.0.0.0:8000