FROM python:3.14-slim

# Set the working directory.
WORKDIR /app

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
RUN uv sync --frozen --no-cache

# Expose the port.
EXPOSE 8000

# Run the application.
CMD ["/app/.venv/bin/uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]