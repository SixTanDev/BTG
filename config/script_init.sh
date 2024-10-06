#!/bin/bash

# Create the __init__.py file to convert the server directory into a Python package
touch __init__.py

# Create symbolic links for 'pyproject.toml' and 'poetry.lock' from the 'config' directory to the current directory
ln -s ./config/pyproject.toml pyproject.toml
ln -s ./config/poetry.lock poetry.lock

# Install all dependencies specified in pyproject.toml without installing the current project package
poetry install --no-interaction --no-ansi --no-root

# Run the database initialization script located at '/server/script_init_db.py'
poetry run python ./config/script_init_db.py

# Start the FastAPI server using Uvicorn, making it accessible from any host on port 8000
poetry run uvicorn app.app:app --host 0.0.0.0 --port 8000
