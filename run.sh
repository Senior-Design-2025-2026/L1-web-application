#!/bin/bash

if [ $# -eq 0 ]; then
  uv run app/app.py
else
  if [ "$1" = "-t" ]; then 
    docker compose up -d --build
  else
    echo "Unknown flag: $1"
    exit 1
  fi
fi
