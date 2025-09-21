#!/bin/bash

if [ $# -eq 0 ]; then
  uv run app/app.py
elif [ "$1" = "--prod" ]; then 
  echo "prod env has not been setup"
elif [ "$1" = "--test" ]; then 
  docker compose up -d --build
else
  echo "Unknown flag: $1"
  exit 1
fi
