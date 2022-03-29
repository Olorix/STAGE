# Environnement de développement

## Installation
1. Installer les dépendances Python 3:
```
pip install pip --upgrade
pip install -r requirements.txt
```
2. Création d'une base de données PostgreSQL (Docker)
```
docker run -d --name django-database -e POSTGRES_PASSWORD=s3cret -p 5432:5432 --rm postgres
```
3. Appliquer les migrations
```
python manage.py migrate
```

## Lancement et configuration
4. Lancer le serveur de développement
```
python manage.py runserver
```
5. Ajouter un compte admin (accès à /admin/)
```
python manage.py createsuperuser
```
