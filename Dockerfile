# Use the Python 3.11 slim image as the base
FROM python:3.11-slim as python-base
ARG CODE_ARTIFACT_TOKEN


ARG LOCAL_USER_ID=1000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

RUN apt-get update && \
    #libs for psycopg2
    apt-get install -y --no-install-recommends gcc g++ libc-dev \
    libpq-dev \
    #libs for trhoubleshooting
   procps curl telnet && \
    rm -rf /var/lib/apt/lists/*

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$PATH"

# User privileges (optional for security)
# Create a new user named 'appuser' with no home directory and no system group
RUN adduser --disabled-password --gecos '' --uid $LOCAL_USER_ID appuser

FROM python-base as builder-base

# Set environment variables
ENV POETRY_VERSION=1.5.1

# Install Poetry globally
RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

# Create and set the working directory
WORKDIR /home/appuser

# Copy just the pyproject.toml and poetry.lock files to leverage Poetry's caching
COPY pyproject.toml poetry.lock ./

# Copy your FastAPI application code into the container
COPY ./app ./app
COPY ./db ./db
COPY alembic.ini entrypoint.sh README.md ./

# Create a virtual environment and install dependencies
RUN poetry install && \
    chmod +x entrypoint.sh && \
    chown -R appuser:appuser /home/appuser && \
    rm -rf /root/.cache

# Expose the port on which your FastAPI application will run (default is 8000)
EXPOSE 8000

# Switch to the 'appuser' user
USER appuser

# Specify the command to run your FastAPI application using Poetry and UVicorn
CMD ["sh", "entrypoint.sh"]