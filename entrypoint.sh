#!/bin/bash

_lint() {
  black .
}

_test() {
  pipenv install --dev --clear --three
  pipenv run pytest tests/
}

action="$INPUT_ACTION"

if [ -z "$action" ]; then
  action="all"
fi

case "$action" in
  "all")
    _lint
    _test
  ;;
  "lint")
    _lint
  ;;
  "test")
    _test
  ;;
  *)
    echo "Unknown action: '$action'"
    exit 1
  ;;
esac
