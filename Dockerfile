# Multi-stage Dockerfile for Affiliate Marketing Website Generator
# Stage 1: Base Python environment with dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        wget \
        ca-certificates \
        gnupg \
        lsb-release \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (for testing generated websites)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development environment
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    ipython \
    jupyter \
    debugpy \
    pre-commit

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p generated templates/output logs

# Set up git for pre-commit (if needed)
RUN git config --global --add safe.directory /app || true

# Install pre-commit hooks (if git repo exists)
RUN if [ -d .git ]; then pre-commit install || true; fi

# Expose port for development server
EXPOSE 8000 5678

# Set up entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "cli.py"]

# Stage 3: Testing environment
FROM development as testing

# Switch back to root for test setup
USER root

# Install additional testing tools
RUN pip install --no-cache-dir \
    pytest-benchmark \
    pytest-xdist \
    pytest-html \
    coverage[toml]

# Install browser dependencies for testing generated websites
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up Chrome/Chromium for Selenium
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

USER app

# Run tests by default in testing stage
CMD ["pytest", "tests/", "-v", "--cov=agents", "--cov=tools", "--cov=cli", "--cov-report=html", "--cov-report=term-missing"]

# Stage 4: Production environment (minimal)
FROM base as production

# Copy only necessary application files
COPY agents/ ./agents/
COPY tools/ ./tools/
COPY config/ ./config/
COPY templates/ ./templates/
COPY cli.py .
COPY requirements.txt .

# Create necessary directories
RUN mkdir -p generated logs

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import agents.website_generator_agent; print('OK')" || exit 1

# Default command
CMD ["python", "cli.py"]