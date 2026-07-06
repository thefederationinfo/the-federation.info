# Build bundle
FROM docker.io/library/node:26 AS build-stage

WORKDIR /app

RUN npm install --global pnpm

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

RUN pnpm install --frozen-lockfile

COPY . .

RUN pnpm build

WORKDIR /app

# Nginx container
FROM docker.io/library/nginx:1.29 AS webserver

COPY --from=build-stage /app/dist /srv/frontend

COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf
