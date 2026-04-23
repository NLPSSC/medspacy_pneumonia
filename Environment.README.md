# Building Environment in Windows (Python 3.9)

python -m pip install invoke && python -m invoke build-pyproject && uv sync --reinstall && uv pip install -e . && uv pip install .[dev,tasks,adjudication] && .venv\Scripts\activate && python -m invoke patch-medpsacy-sentence-splitting