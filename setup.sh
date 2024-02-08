#!/bin/bash

# Install Poetry
echo "Installing Poetry..."
python3.11 -m pip install poetry

# Install Dependencies
echo "Installing project dependencies..."
python3.11 -m poetry install

# Install Pre-Commit
echo "Installing Pre-Commit hooks..."
python3.11 -m poetry run pre-commit install

# Sync Lock File
echo "Syncing lock file..."
python3.11 -m poetry lock --no-update

# Setup CI Test Requirements
echo "Exporting CI test requirements..."
python3.11 -m poetry export --with dev --with test --without-hashes -f requirements.txt --output ci-test-requirements.txt

# Enter Poetry shell
echo "Entering Poetry shell..."
python3.11 -m poetry shell

echo "Setup completed."
