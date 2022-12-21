#!/bin/bash
set -e

rm -rf dist
python -m build --sdist .
python -m twine check dist/*
twine upload --skip-existing dist/*
