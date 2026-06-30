.RECIPEPREFIX := >

.PHONY: install dev lint test build

install:
>npm install

dev:
>npm run dev -- --host 0.0.0.0 --port $${FRONTEND_PORT:-3000}

lint:
>npm run lint

test:
>npm run test

build:
>npm run build
