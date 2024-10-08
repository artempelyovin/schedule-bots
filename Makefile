SHELL := /bin/bash
PROJECT_DIR ?= $(shell git rev-parse --show-toplevel)


.PHONY: install-dev
install-dev:
	poetry env use 3.11
	poetry install --with dev
	poetry run pre-commit install --install-hooks --hook-type pre-commit --hook-type commit-msg


.PHONY: activate-env
activate-env:
	poetry shell


.PHONY: format
format:
	poetry run ruff format $(PROJECT_DIR)/src  # run `black`
	poetry run ruff check $(PROJECT_DIR)/src --select I --fix   # run `isort`


.PHONY: lint
lint:
	poetry run ruff check $(PROJECT_DIR)/src/
	poetry run mypy $(PROJECT_DIR)/src/
