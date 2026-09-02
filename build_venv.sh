#!/usr/bin/env bash
rm -rf .venv

/c/Windows/py.exe -3.13 -m venv .venv
source .venv/Scripts/activate

python -m pip install --upgrade pip
python -m pip install uv
python -m pip install -e ".[dev]"