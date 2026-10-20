.PHONY: install install-dev lint format typecheck test coverage benchmarks clean

install:            ## Install runtime dependencies
	pip install -e .

install-dev:        ## Install with dev + test tooling
	pip install -e ".[dev]"

lint:               ## Run ruff checks
	ruff check src tests benchmarks scripts

format:             ## Format code with black + ruff
	ruff format src tests benchmarks scripts
	black src tests benchmarks scripts

typecheck:          ## Run mypy
	mypy src

test:               ## Run the test suite
	pytest

coverage:           ## Run tests with coverage report
	pytest --cov=aisafety --cov-report=term-missing

benchmarks:         ## Run the fast (no-network) benchmark smoke tests
	pytest benchmarks -m "not network"

datasets:           ## Download the real public datasets used by harnesses
	python scripts/download_datasets.py --all

report:             ## Generate a markdown safety report from latest results
	python scripts/generate_report.py --results results/

clean:              ## Remove caches and build artifacts
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

help:               ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
