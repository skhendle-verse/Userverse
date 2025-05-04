# 
FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 
WORKDIR /code

# 
COPY ./pyproject.toml /code/pyproject.toml

# 

RUN uv sync

# 
COPY ./app /code/app

#
EXPOSE 8200

# 
CMD ["sh", "-c", "while true; do uv run uvicorn app.main:app --port 8500  --env production   --config sample-config.json  --host 0.0.0.0; done"]