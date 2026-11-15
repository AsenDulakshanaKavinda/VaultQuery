.PHONY: build run test test-cover clean lint

# Go parameters
GOCMD=go
GOBUILD=$(GOCMD) build
GOTEST=$(GOCMD) test
GOCLEAN=$(GOCMD) clean
BINARY_NAME=auth-api
MAIN_PATH=cmd/api/main.go

# Build the application
build:
	@echo "Building binary..."
	$(GOBUILD) -o bin/$(BINARY_NAME) $(MAIN_PATH)

# Run the application locally
run:
	@echo "Starting application..."
	$(GOBUILD) -o bin/$(BINARY_NAME) $(MAIN_PATH)
	./bin/$(BINARY_NAME)

# Run tests safely by ensuring subpackages can locate the .env file during init()
test:
	@echo "Running tests..."
	@if [ -f .env ]; then cp .env internal/services/.env; fi
	$(GOTEST) -v ./...
	@if [ -f internal/services/.env ]; then rm internal/services/.env; fi

# Run tests with code coverage report
test-cover:
	@echo "Running tests with coverage..."
	@if [ -f .env ]; then cp .env internal/services/.env; fi
	$(GOTEST) -coverprofile=coverage.out ./...
	$(GOCMD) tool cover -html=coverage.out -o coverage.html
	@if [ -f internal/services/.env ]; then rm internal/services/.env; fi
	@echo "Coverage report generated: coverage.html"

# Clean up build artifacts and coverage files
clean:
	@echo "Cleaning up..."
	$(GOCLEAN)
	rm -rf bin/
	rm -f coverage.out coverage.html
	find internal/ -name ".env" -delete

docker-build:
	@echo "building docker image..."
	docker build -t vlt-auth-service:latest .

docker-image-run:
	@echo "running docker image..."
	docker run -d   -p 8080:8080   -e ENV=development   -e PORT=8080   -e DATABASE_URL=<db url>  -e SECRET_JWT_KEY=<key>  -e SECRET_REFRESH_KEY=<key>  --name vlt-auth-container   vlt-auth-service:latest

