# List all commands
list:
    just -l


# Run in dev mode
run:
    uv run --env-file ../.env.air fastapi dev


# Ingest files
run:
    uv run --env-file ../.env.air scripts/ingest.py