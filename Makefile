.PHONY: help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

test:  ## Run unit tests
	@pytest -x tests/

coverage: ## Run unit tests coverage
	@pytest -x --cov bank_account_validator/ --cov-report=xml --cov-report=term-missing tests/
