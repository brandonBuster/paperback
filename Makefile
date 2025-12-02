# Makefile for paperback Docker operations

# Docker image name
IMAGE = paperback

# Default script (can be overridden)
SCRIPT ?= run.py

# Run a Python script in Docker
# Usage: make run SCRIPT=quickstart.py
# Usage: make run SCRIPT=get_alpaca_quote.py
run:
	@echo "Running $(SCRIPT) in Docker..."
	docker run --rm -v $(PWD):/app $(IMAGE) python $(SCRIPT)

# Rebuild the Docker image
build:
	@echo "Building Docker image..."
	DOCKER_BUILDKIT=1 docker build -t $(IMAGE) .

# Run with output directory mounted
run-with-output:
	@echo "Running $(SCRIPT) in Docker with output directory..."
	docker run --rm -v $(PWD):/app -v $(PWD)/output:/app/output $(IMAGE) python $(SCRIPT)

# Run quickstart.py
quickstart:
	$(MAKE) run SCRIPT=quickstart.py

# Run get_alpaca_quote.py
alpaca-quote:
	$(MAKE) run SCRIPT=get_alpaca_quote.py

# Run alpaca_historical.py
alpaca-historical:
	$(MAKE) run SCRIPT=alpaca_historical.py

alpaca-crypto:
	$(MAKE) run SCRIPT=alpaca_crypto.py

# Run the default run.py
default:
	$(MAKE) run-with-output SCRIPT=run.py

# Show help
help:
	@echo "Available targets:"
	@echo "  make run SCRIPT=<script.py>  - Run any Python script in Docker"
	@echo "  make build                   - Rebuild the Docker image"
	@echo "  make quickstart              - Run quickstart.py"
	@echo "  make alpaca-quote           - Run get_alpaca_quote.py"
	@echo "  make alpaca-historical      - Run alpaca_historical.py"
	@echo "  make alpaca-crypto      	- Run alpaca_crypto.py"
	@echo "  make default                - Run run.py with output directory"
	@echo ""
	@echo "Examples:"
	@echo "  make run SCRIPT=quickstart.py"
	@echo "  make run SCRIPT=get_alpaca_quote.py"

.PHONY: run build run-with-output quickstart alpaca-quote alpaca-historical default help

