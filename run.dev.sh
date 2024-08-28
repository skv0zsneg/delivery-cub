#!/bin/bash
if [ "$1" = "down" ]; then
    docker compose -f docker-compose.dev.yml down
else
    export $(grep -v '^#' .env.dev | xargs -d '\n')
    docker compose -f docker-compose.dev.yml up -d --build
fi
