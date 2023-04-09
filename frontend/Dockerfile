#Build le projet Vue
FROM node:12.18.1-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
RUN npm i axios
RUN npm i vue-axios
COPY . .
RUN npm run build

#Créer le serveur Nginx
FROM nginx:1.19.0-alpine AS prod-stage
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]