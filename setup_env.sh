#!/bin/bash

# Check if .env file exists; if not, create an empty one
if [ ! -f .env ]; then
    echo "Creating empty .env file"
    touch .env
else
    echo ".env file already exists"
fi