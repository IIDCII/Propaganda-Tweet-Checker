# --- SETTINGS ---
# We use the 'api' folder as the build context for the Dev Shell 
# because it contains our "Master Workshop" Dockerfile.
COMPOSE_DEV = docker compose -f docker-compose.yml -f docker-compose.override.yml
COMPOSE_PROD = docker compose -f docker-compose.yml

.PHONY: up shell test-int train build-prod clean help

# --- DEVELOPMENT ---

# Start the background infrastructure (DB, API, ML Service)
# This uses 'docker-compose.override.yml' by default to enable live-reloading.
up:
	@echo "🚀 Starting background services..."
	$(COMPOSE_DEV) up -d db ml_service api

# Enter the Master Dev Shell (The Neovim/LazyVim environment)
# This will automatically call 'up' to ensure your DB is ready.
shell: up
	@echo "💻 Entering Unified Dev Shell..."
	$(COMPOSE_DEV) run --rm dev-shell zsh

# --- TESTING & ML ---

# Run Integration Tests across all containers
# This uses the 'tester' container from the 'tools' profile.
test-int:
	@echo "🧪 Running Integration Tests..."
	$(COMPOSE_DEV) --profile tools run --rm tester

# Run the ML Training job
# This spins up the 'training' container, runs the script, and shuts down.
train:
	@echo "🧠 Starting ML Training Job..."
	$(COMPOSE_DEV) --profile tools run --rm training

# --- PRODUCTION VERIFICATION ---

# Build and run the SLIM production images locally.
# Use this to verify that the 'production' target works before pushing to AWS.
build-prod:
	@echo "📦 Building slim production images..."
	$(COMPOSE_PROD) build
	@echo "🚀 Running production-ready stack..."
	$(COMPOSE_PROD) up -d

# --- UTILS ---

# Wipe all containers and volumes (Fresh start)
clean:
	@echo "🧹 Cleaning up containers and volumes..."
	$(COMPOSE_DEV) down -v

help:
	@echo "Available commands:"
	@echo "  make up         - Start DB, API, and ML services in background"
	@echo "  make shell      - Enter the Nvim/LazyVim dev shell"
	@echo "  make test-int   - Run cross-container integration tests"
	@echo "  make train      - Run the ML training container"
	@echo "  make build-prod - Build and test slim production images"
	@echo "  make clean      - Remove all containers and volumes"
