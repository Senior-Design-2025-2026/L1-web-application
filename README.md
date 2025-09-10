# L1-web-server

Web server + gui for University of Iowa Senior Design Lab 1: Thermometer

# Project Setup

## Setting up the Project
We dont have to use uv, however it is <= 10x times faster than pip... and you dont need to set up venv. 'uv run' handles the environment setup for you.
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

## Checking and Correcting Syntax with Ruff
optional, but this is nice for cleaning imports and small formatting issues. uv is a far simpler alternative to pipx for tooling. Ruff has many common python code cleansers packaged and runs super fast.
1. Install `ruff`:
   ```sh
   pip install ruff
   ```
2. Check for syntax issues:
   ```sh
   ruff check .
   ```
3. Automatically fix issues:
   ```sh
   ruff check . --fix
   ```
