# Use official Python image as builder image
# Use slim version for smaller image size
FROM python:3.12-slim AS builder

# Install poetry
RUN pip install poetry==2.1.3
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Create venv
COPY app/pyproject.toml app/poetry.lock app/README.md ./
COPY app/pynuzel_bot ./pynuzel_bot
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev

# Second Pyton image used for run time
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy poetry venv from builder image
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the rest of the app code
COPY app/ ./

# Run the application
ENTRYPOINT ["python", "-m", "main"]