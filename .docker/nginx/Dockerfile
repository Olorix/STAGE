FROM nginx:1.21.0-alpine

# Récupère bash pour wait-for-it
RUN apk update && apk add bash

# Récupère le fichier de configuration
COPY .docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copie les scripts de lancement
COPY .docker/shared/wait-for-it.sh /usr/src/wait-for-it.sh

WORKDIR /usr/src

# Une fois que Gunicorn est démarré, lance nginx
CMD ["./wait-for-it.sh", "gunicorn:8000", "--", "nginx", "-g", "daemon off;"]
