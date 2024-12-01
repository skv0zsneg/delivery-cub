#!/usr/bin/env bash

printf "Start running lint...\n\n"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_PATH=$SCRIPT_DIR/../
LINTER_CONFIG_PATH=$APP_PATH/configs/linters/

printf "Black checking...\n"
black --config=$LINTER_CONFIG_PATH/pyproject.toml $APP_PATH
printf "Done.\n\n"

printf "isort checking...\n"
isort --settings-path=$LINTER_CONFIG_PATH/isort.cfg $APP_PATH
printf "Done.\n\n"

printf "All Done.\n"