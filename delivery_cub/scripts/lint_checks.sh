#!/usr/bin/env bash

printf "Start lint checking...\n\n"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_PATH=$SCRIPT_DIR/..
LINTER_CONFIG_PATH=$APP_PATH/configs/linters/

printf "MyPy checking...\n"
mypy --config-file=$LINTER_CONFIG_PATH/mypy.ini $APP_PATH
printf "Done.\n\n"

printf "Black checking...\n"
black --config=$LINTER_CONFIG_PATH/pyproject.toml --check $APP_PATH
printf "Done.\n\n"

printf "flake8 checking...\n"
flake8 --config=$LINTER_CONFIG_PATH/flake8.ini $APP_PATH
printf "Done.\n\n"

printf "isort checking...\n"
isort --settings-path=$LINTER_CONFIG_PATH/isort.cfg --check-only $APP_PATH
printf "Done.\n\n"

printf "All Done.\n"