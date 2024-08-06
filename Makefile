.DEFAULT_GOAL := help

.PHONY: help
help: ## Show help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: ## Initialize project
	poetry install
	poetry run pre-commit install

.PHONY: lint
lint: ## Code analyse and lint
	poetry run pylint src/ tests/

.PHONY: test
test: ## Run tests
	poetry run pytest --cov=src --cov-report=term-missing

.PHONY: tox
tox: ## Run tox
	poetry run tox

.PHONY: build
build: ## Build project
	poetry build


.PHONY: compile
compile: ## Compile Python files
	poetry run python setup.py build_ext --build-lib build
	cp ./src/stbl/__cli__.py ./build/stbl/



.PHONY: bundle
bundle: ## Bundle project with pyinstaller
	rm -rf build/ dist/
	poetry run pyinstaller stbl.spec

	cp {CHANGELOG.md,LICENSE,README.md} dist/



.PHONY: publish
publish: build ## Publish project
	poetry publish --build

.PHONY: codecov
codecov: ## Upload coverage.xml to codecov.com
	poetry run pytest --cov=src --cov-report=xml
	codecov

.PHONY: clean
clean: ## Clean up cache files
	find . -name '__pycache__' -type d | xargs rm -rf
	rm -rf .pytest_cache/ .tox/ build/ dist/
	rm -f .coverage coverage.xml .python_version
