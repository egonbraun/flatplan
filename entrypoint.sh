#!/bin/bash

_build() {
  poetry build --ansi
}

_init() {
  poetry install --remove-untracked --no-root --ansi
}

_lint() {
  poetry run black .
}

_run() {
  poetry run flatplan --debug --jsonplan=tests/assets/plan.json
}

_test() {
  poetry run pytest tests/
}

action="all"

if [  "$ENTRYPOINT_ACTION" != "" ]; then
  action="$ENTRYPOINT_ACTION"
fi

if [ "$1" != "" ]; then
  action="$1"
fi

_init

case "$action" in
  "all")
    _lint
    _test
    _build
  ;;
  "build")
    _build
  ;;
  "lint")
    _lint
  ;;
  "run")
    _run
  ;;
  "test")
    _test
  ;;
  *)
    echo "Unknown action: '$action'"
    exit 1
  ;;
esac
