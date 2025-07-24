#!/bin/bash
set -e

# Docker entrypoint script for Affiliate Marketing Website Generator

echo "🚀 Starting Affiliate Marketing Website Generator..."

# Check if running in development mode
if [ "$ENVIRONMENT" = "development" ]; then
    echo "📝 Development mode detected"
    
    # Install development dependencies if needed
    if [ ! -f "/app/.dev-deps-installed" ]; then
        echo "Installing development dependencies..."
        pip install -e . 2>/dev/null || true
        touch /app/.dev-deps-installed
    fi
    
    # Set up pre-commit hooks if in git repo
    if [ -d "/app/.git" ] && [ ! -f "/app/.git/hooks/pre-commit" ]; then
        echo "Setting up pre-commit hooks..."
        pre-commit install 2>/dev/null || true
    fi
fi

# Check if running tests
if [ "$1" = "test" ]; then
    echo "🧪 Running test suite..."
    shift
    exec pytest tests/ -v --cov=agents --cov=tools --cov=cli --cov-report=term-missing "$@"
fi

# Check if running linting
if [ "$1" = "lint" ]; then
    echo "🔍 Running code quality checks..."
    echo "Running ruff..."
    ruff check . || true
    echo "Running mypy..."
    mypy . || true
    echo "Running black check..."
    black --check . || true
    exit 0
fi

# Check if running interactive mode
if [ "$1" = "cli" ] || [ "$1" = "interactive" ]; then
    echo "💬 Starting interactive CLI..."
    exec python cli.py
fi

# Check if running specific agent
if [ "$1" = "generate" ]; then
    echo "🎨 Running website generation..."
    shift
    exec python -c "
import asyncio
from agents.website_generator_agent import WebsiteGeneratorAgent
from agents.models import GoogleSheetsConfig, WebsiteGenerationRequest, NicheType, AgentDependencies

async def main():
    generator = WebsiteGeneratorAgent()
    
    # Example generation - replace with CLI args parsing if needed
    sheets_config = GoogleSheetsConfig(sheet_id='demo_sheet_id')
    request = WebsiteGenerationRequest(
        niche=NicheType.TECH,
        brand_name='Demo Brand',
        target_audience='Demo audience',
        sheets_config=sheets_config
    )
    
    deps = AgentDependencies()
    result = await generator.generate_complete_website(request, deps)
    print(f'Website generated: {result.project_name}')

asyncio.run(main())
"
fi

# Wait for dependencies if specified
if [ -n "$WAIT_FOR_SERVICES" ]; then
    echo "⏳ Waiting for services: $WAIT_FOR_SERVICES"
    
    for service in ${WAIT_FOR_SERVICES//,/ }; do
        echo "Waiting for $service..."
        while ! nc -z $service 2>/dev/null; do
            sleep 1
        done
        echo "$service is ready!"
    done
fi

# Set up logging
if [ -n "$LOG_LEVEL" ]; then
    export PYTHONPATH="/app:$PYTHONPATH"
    echo "📋 Log level set to: $LOG_LEVEL"
fi

# Create necessary directories
mkdir -p /app/generated /app/logs

# Set proper file permissions
if [ "$(id -u)" = "0" ]; then
    # Running as root, fix permissions
    chown -R app:app /app/generated /app/logs 2>/dev/null || true
fi

# Handle different run modes
case "$1" in
    "bash"|"shell")
        echo "🐚 Starting bash shell..."
        exec /bin/bash
        ;;
    "python")
        echo "🐍 Starting Python interpreter..."
        shift
        exec python "$@"
        ;;
    "debug")
        echo "🐛 Starting debug mode..."
        exec python -m debugpy --listen 0.0.0.0:5678 --wait-for-client cli.py
        ;;
    "")
        echo "🚀 Starting default application..."
        exec python cli.py
        ;;
    *)
        echo "📋 Executing custom command: $@"
        exec "$@"
        ;;
esac