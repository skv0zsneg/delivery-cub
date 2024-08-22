#!/bin/bash
if [ "$1" = "down" ]; then
    docker compose -f docker-compose.dev.yml down
else
    export $(grep -v '^#' .env.dev | xargs -d '\n')
    echo "I was here!"
    docker compose -f docker-compose.dev.yml up -d --build
fi
