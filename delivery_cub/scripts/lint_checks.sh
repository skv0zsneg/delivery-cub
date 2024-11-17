#!/usr/bin/env bash

printf "Start lint checking...\n\n"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APP_PATH=$SCRIPT_DIR/../

printf "MyPy checking...\n"
mypy --config-file=$APP_PATH/configs/mypy.ini $APP_PATH
printf "Done.\n\n"

printf "Black checking...\n"
black --check $APP_PATH
printf "Done.\n\n"

printf "flake8 checking...\n"
flake8 --max-line-length 99 $APP_PATH
printf "Done.\n\n"

printf "isort checking...\n"
isort --check-only --profile=black $APP_PATH
printf "Done.\n\n"

printf "All Done.\n"