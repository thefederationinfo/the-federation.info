# Build bundle
FROM docker.io/library/node:24 AS build-stage

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . .

RUN yarn build

WORKDIR /app

# Nginx container
FROM docker.io/library/nginx:1.29 AS webserver

COPY --from=build-stage /app/dist /srv/frontend

COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf
