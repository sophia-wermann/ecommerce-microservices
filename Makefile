.PHONY: up down build logs ps clean

## Start all services in detached mode (build images if needed)
up:
	docker-compose up --build -d

## Start all services and follow logs
up-logs:
	docker-compose up --build

## Stop and remove all containers
down:
	docker-compose down

## Stop containers and remove volumes (clears all data)
down-volumes:
	docker-compose down -v

## Rebuild all images without cache
build:
	docker-compose build --no-cache

## Follow logs of all services
logs:
	docker-compose logs -f

## Follow logs of a specific service: make logs-service s=catalog-service
logs-service:
	docker-compose logs -f $(s)

## Show running containers
ps:
	docker-compose ps
