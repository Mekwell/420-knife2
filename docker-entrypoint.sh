#!/bin/sh

if [ ! -f "data/users.db" ]; then
  mkdir -p data
  flask shell <<EOF
from app import db, create_app
app = create_app()
with app.app_context():
    db.create_all()
EOF
fi

exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - app:app
