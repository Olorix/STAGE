FROM python:3.8-alpine

# Installe les dépendances de PostgreSQL (psycopg2)
RUN apk update && apk add postgresql-dev \
  python3-dev musl-dev gcc g++ bash

# Désactive l'écriture en bytecode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installe les dépendances Python
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie les scripts de lancement
COPY .docker/shared/wait-for-it.sh /usr/src/wait-for-it.sh
COPY .docker/gunicorn/entrypoint.sh /usr/src/entrypoint.sh

# Copie le code source
COPY src /usr/src

# Prépare le répertoire des fichiers statiques
RUN mkdir /var/staticfiles

# Utilise un utilisateur non-root
RUN adduser django -D --no-create-home
RUN chown -R django:django /usr/src /var/staticfiles
USER django

WORKDIR /usr/src

# Compile les feuilles de styles
RUN python manage.py sass paf/static/paf/scss/custom-bootstrap.scss paf/static/paf/css/custom-bootstrap.css -t compressed

# Migre les fichiers statiques
RUN python manage.py collectstatic --no-input

CMD ["./entrypoint.sh"]
