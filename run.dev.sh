#!/bin/bash
if [ "$1" = "down" ]; then
    docker compose -f docker-compose.dev.yml down
else
    source .env.dev
    docker compose -f docker-compose.dev.yml up -d --build
fi
