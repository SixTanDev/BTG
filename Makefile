# Variables
DOCKER_COMPOSE_FILE := dockercompose.yml

# Build the Docker image and services using Docker Compose
build:
	@echo "Building the Docker containers..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) build

# Start the services in detached mode
up:
	@echo "Starting the Docker containers..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop the services
down:
	@echo "Stopping the Docker containers..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Show the logs of the running containers
logs:
	@echo "Showing the logs of the Docker containers..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f

# Stop and remove containers, networks, and volumes
clean:
	@echo "Stopping and cleaning up the Docker containers, networks, and volumes..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) down --volumes --remove-orphans

# Run build, up, and logs in sequence
start: build up logs
	@echo "Docker containers are up and running."

# Run build and up in sequence
build-up: build up
	@echo "Build and start processes completed."

# Ejecutar pre-commit para verificar que los hooks funcionan
pre-commit-check:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files --hook-stage pre-commit
	pre-commit run --all-files --hook-stage pre-push

# Help command to list available options
help:
	@echo "Makefile options:"
	@echo "  build             - Build the Docker images and containers"
	@echo "  up                - Start the Docker containers in detached mode"
	@echo "  down              - Stop the Docker containers"
	@echo "  logs              - Show the logs from the running Docker containers"
	@echo "  clean             - Stop and remove containers, networks, and volumes"
	@echo "  start             - Build, start, and show the logs for the containers"
	@echo "  build-up          - Build the Docker images and start the containers"
	@echo "  pre-commit-check  - Run pre-commit hooks to check if they are working"
	@echo "  help              - Show this help message"
