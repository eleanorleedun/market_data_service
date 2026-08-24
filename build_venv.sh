#!/usr/bin/env bash
rm -rf .venv

/c/Windows/py.exe -3.13 -m venv .venv
source .venv/Scripts/activate

python -m pip install --upgrade pip

python --version
python -m pip --version
python -c "import sys, platform, sysconfig; print('executable:', sys.executable); print('platform:', sys.platform); print('machine:', platform.machine()); print('platform tag:', sysconfig.get_platform())"

python -m pip install uv
python -m pip install -e ".[dev]"
