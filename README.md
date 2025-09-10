# L1-web-server

Web server + gui for University of Iowa Senior Design Lab 1: Thermometer

# Project Setup

## Setting up the Project
Using UV as package manager (<= 10x faster than pip! also handles venv)

1. Ensure you have Python 3.12 or later installed.
2. Install `uv` globally:
   ```sh
   pip install uv
   ```
3. Sync dependencies from `pyproject.toml`:
   ```sh
   uv sync
   ```
4. Run the application:
   ```sh
   uv run app/app.py
   ```

UV Documentation: https://docs.astral.sh/uv/

## Checking and Correcting Syntax with Ruff
Optional code quality check using Ruff 

1. Install `ruff`:
   ```sh
   uv add --dev ruff # this is done
   ```
2. Check for syntax issues:
   ```sh
   uv run ruff check
   ```
3. Automatically fix issues:
   ```sh
   uv ruff check --fix
   ```

Ruff documentation: https://docs.astral.sh/ruff/
