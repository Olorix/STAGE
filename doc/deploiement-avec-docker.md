# Déploiement avec Docker
L'application [mon-paf](https://gogs.in.ac-amiens.fr/jducange/mon-paf) a été créée pour être déployée en utilisant [Docker](https://www.docker.com) via [Docker-compose](https://docs.docker.com/compose). Avant de continuer assurer vous de ces 2 programmes sont installés et que vous possédez les droits suffisants pour les utiliser.

> Toutes les commandes de ce guide assument que vous vous situez à la racine du du dépôt. Pensez à vous y placer avant de commencer.

## Compatibilité et versions
Le fichier `docker-compose.yml` est rédigé en *version 3.5* compatible avec un *docker-engine 17.12.0 ou plus*. Vous pouvez vérifier votre version de `docker` à l'aide de la commande:
```shell
# Affiche la version de Docker
$ docker --version
```
> En cas de doute vous pouvez consulter [cette page](https://docs.docker.com/compose/compose-file/compose-versioning). À titre d'information l'outil a été développé avec *docker 18.09.0* *docker-compose 1.22.0*.

## Installation
Dans un premier temps il s'agit de récupèrer le code de l'application, pour cela on peut directement `git clone` le dépôt dans le répertoire de déploiement.
```shell
# Récupère le code-source de l'application
$ git clone https://gogs.in.ac-amiens.fr/jducange/mon-paf.git

# Se déplace à la racine du dépôt
$ cd mon-paf
```

Le paramètrage de l'application repose en grande partie sur un fichier `.env` en clonant le dépôt vous avez également cloné un fichier `.env-example`. Il s'agit d'un exemple que vous pourrez utiliser comme référence.
```env
# Paramètrage de la base PostgreSQL
POSTGRES_USER=django # Nom d'utilisateur
POSTGRES_PASSWORD=s3cret # Mot de passe
POSTGRES_DB=django # Nom de la base de données

# Paramètrage du compte admin par défaut de Django
DJANGO_SUPERUSER_USERNAME=admin # Nom d'utilisateur
DJANGO_SUPERUSER_EMAIL=jules.ducange@ac-amiens.fr # Email
DJANGO_SUPERUSER_PASSWORD=9ZyhG7h5Uu@ndaBv$qVEz*vP # Mot de passe

# Clée secrète (Fonctionnement interne de Django)
SECRET_KEY=django-insecure-zls&-8_%jblts+^eput8$1+jqb-$a@zd#wtvmwpawgewt50s^8

# Stage de déploiement [DEVELOPMENT, PRODUCTION]
STAGE=DEVELOPMENT

# URL de l'application
ROOT_URL=paf
```
> Quand le `STAGE=DEVELOPMENT` le mode **DEBUG** de Django est activé et les erreurs seront plus facile à disgnostiquer.

## Configuration
Quand le mode **DEBUG** est désactivé, Django filtre les requêtes et ne réponds uniquement qu'à celles dont l'hôte apparaît dans la liste des `ALLOWED_HOST` dans le module `src/django_core/settings.py` :
```python
# Autorise '127.0.0.1' et 'localhost'
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]
```
### Modifier l'url de l'application
L'application se divise en 2 parties distinctes `paf/` l'application elle-même et `admin/` le site d'administration. Si vous avez besoin de changer l'url de l'application en elle même vous pouvez changer la variable `ROOT_URL`. **Attention**: la configuration de Nginx ne prend pas en compte la variable `ROOT_URL` il faut effectuer le changer directement dans le fichier `.docker/nginx/default.conf`.

Par exemple pour changer l'url de l'application pour `mon-paf/`. Il faudra modifier le fichier de configuration de nginx pour qu'il ressemble à :
```nginx
  location /mon-paf/static/ {
    alias /var/staticfiles/;
  }
```

## Lancer l'application
Pour construire les conteneurs et lancer l'application vous pouvez utiliser la commande:
```shell
# Construit et lance les conteneurs
$ docker-compose up --detach --build
```
À ce niveau l'application devrait-être disponible à `adresse-du-serveur/paf`.

> **Attention**: Pour des raisons de sécurité tout les fichiers nécessaires au fonctionnement de l'application sont copiés à la compilation de l'image. Si jamais vous souhaitez modifier certains fichier, n'oubliez pas de re-compiler les conteneurs avec l'option `--build` après coup pour que vos changements prennent effet.
