#!/bin/bash
if [ "$1" = "down" ]; then
    docker compose -f docker-compose.prod.yml down
else
    export $(grep -v '^#' .env.prod | xargs -d '\n')
    docker compose -f docker-compose.prod.yml up -d --build
fi
