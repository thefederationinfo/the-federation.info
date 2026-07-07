# list available recipes
default:
    @just --list

# run backend and frontend tests
test: backend-test frontend-test

# run the backend test suite (live tests excluded, run those with pytest -m live)
backend-test:
    pytest -m "not live"

# run the frontend unit tests
frontend-test:
    pnpm run test

# lint backend and frontend
lint: backend-lint frontend-lint

# lint the python code
backend-lint:
    ruff check .

# lint the frontend code
frontend-lint:
    pnpm run lint

# format backend and frontend
format: backend-format frontend-format

# format the python code
backend-format:
    ruff format .

# format the frontend code
frontend-format:
    pnpm run format

# frontend dev server against a local hasura (docker-compose up)
dev:
    pnpm run dev

# frontend dev server against the live https://the-federation.info GraphQL API
dev-live:
    LIVE_GRAPHQL=1 pnpm run dev
