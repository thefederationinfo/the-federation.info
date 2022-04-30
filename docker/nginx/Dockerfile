# Build bundle
FROM node:16 as build-stage

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . .

RUN yarn build

WORKDIR /app

# Nginx container
FROM nginx

COPY --from=build-stage /app/dist /srv/frontend

COPY docker/nginx/nginx.conf /etc/nginx/conf.d/thefederation.conf
