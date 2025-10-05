# List all commands
list:
    just -l


# Run in dev mode
run:
    uv run --env-file ../.env.air fastapi dev


# Ingest files
ingest path:
    uv run --env-file ../.env.air ingest.py {{path}}


# Search
search query:
    uv run --env-file ../.env.air script.py {{query}}