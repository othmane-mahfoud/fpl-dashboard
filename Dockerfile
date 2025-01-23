# Use Python 3.13-alpine as the base image
FROM python:3.13-alpine

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only the pyproject.toml and poetry.lock for dependency installation
COPY pyproject.toml poetry.lock ./

# Validate pyproject.toml and install dependencies
RUN poetry check \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

# Copy the rest of the application files
COPY . .

# Expose the port the app runs on
EXPOSE 8050

# Run the application
CMD ["poetry", "run", "python", "app.py"]