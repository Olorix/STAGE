#!/usr/bin/env bash

# Attends la réponse de PostreSQL
./wait-for-it.sh postgres:5432

# Si la base de données est accessible
if [[ $? -eq 0 ]]; then

  # Applique les migrations de la base de données
  echo "Migrating database schemes..."
  python manage.py migrate --no-input
  echo

  # Créer l'utilisateur dafpen
  echo "Creating admin account"
  python manage.py createsuperuser --noinput
  echo

  # Lance le serveur Gunicorn
  echo "Starting gunicorn server..."
  gunicorn django_core.wsgi --bind 0.0.0.0:8000 --timeout 300
  echo

fi
