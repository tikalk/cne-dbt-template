echo "Seting up vscode"
mkdir -p /home/$USERNAME/.vscode

echo "Seting up venv"
uv venv
uv sync
pre-commit install
pre-commit install --hook-type pre-commit --hook-type pre-push
pre-commit install-hooks
pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks
