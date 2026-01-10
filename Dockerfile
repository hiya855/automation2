# --- Stage 1: Build Stage ---
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies for psycopg2 (if needed)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to a local folder
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# --- Stage 2: Final Runtime Stage ---
FROM python:3.11-slim

WORKDIR /app

# Install only the runtime library for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy the installed python packages from the builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Update PATH so the app can find the installed packages
ENV PATH=/root/.local/bin:$PATH

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]
