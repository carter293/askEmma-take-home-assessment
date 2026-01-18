# Policy Ingestion

Vectorizes policy documents and stores them in SQLite with sqlite-vec for semantic search.

## Prerequisites

- Python with SQLite extension support (see Platform Notes below)
- OpenAI API key in `.env` file

## Setup

```bash
uv sync
```

## Run

```bash
uv run ingestion/ingestion.py
```

## How it works

1. Reads policy files from `policies/` directory
2. Generates example situations for each policy using GPT-4
3. Creates embeddings for the situations
4. Stores policies and embeddings in `db/askEmma.sqlite`

## Platform Notes

### macOS

The default Python on macOS does not support SQLite extensions. Use Homebrew Python instead:

```bash
# Install Homebrew Python if needed
brew install python

# Recreate virtual environment with Homebrew Python
uv venv --python /opt/homebrew/bin/python3 --clear
uv sync
```

**Why this is needed:** macOS ships with a version of SQLite that doesn't allow loading extensions, and pyenv-installed Python also lacks the `--enable-loadable-sqlite-extensions` compilation flag.

### Linux/Dev Containers

Python on Linux (Debian, Ubuntu, etc.) typically has SQLite extension support enabled by default. The Microsoft devcontainer Python images (`mcr.microsoft.com/devcontainers/python`) work out of the box.
