# Dockerfile pour Nexus Réussite Frontend
FROM node:18-alpine as build

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de package
COPY package*.json ./

# Installer les dépendances
RUN npm ci --only=production

# Copier le code source
COPY . .

# Construire l'application
RUN npm run build

# Stage de production avec Nginx
FROM nginx:alpine

# Copier la configuration Nginx personnalisée
COPY nginx.conf /etc/nginx/nginx.conf

# Copier les fichiers construits
COPY --from=build /app/dist /usr/share/nginx/html

# Copier le script d'entrée
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Exposer le port
EXPOSE 80

# Commande de santé
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Point d'entrée
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

