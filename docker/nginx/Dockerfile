# Build bundle
FROM node:9 as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm i

COPY . .

RUN npm run build

WORKDIR /app

# Nginx container
FROM nginx

COPY --from=build-stage /app/dist /srv/frontend

ARG env

COPY docker/nginx/nginx_$env.conf /etc/nginx/conf.d/thefederation.conf
