#!/bin/sh -e
set -x

ruff format src tests
ruff check --fix src tests

mypy src tests

pytest -v tests