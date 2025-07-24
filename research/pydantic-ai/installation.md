# Pydantic AI Installation Guide

## Requirements
- Python 3.9+
- PyPI package: `pydantic-ai`

## Basic Installation
```bash
pip install pydantic-ai
# or
uv add pydantic-ai
```

## Optional Installations

### With Pydantic Logfire
```bash
pip install "pydantic-ai[logfire]"
# or
uv add "pydantic-ai[logfire]"
```

### With Examples
```bash
pip install "pydantic-ai[examples]"
# or
uv add "pydantic-ai[examples]"
```

## Slim Install (Model-Specific)
```bash
pip install "pydantic-ai-slim[openai]"
# or
uv add "pydantic-ai-slim[openai]"
```

## Slim Install Optional Groups
- `logfire`
- `evals`
- `openai`
- `vertexai`
- `anthropic`
- `groq`
- `mistral`
- `cohere`
- `duckduckgo`
- `tavily`
- `ag-ui`

## Multi-Model/Use Case Example
```bash
pip install "pydantic-ai-slim[openai,vertexai,logfire]"
# or
uv add "pydantic-ai-slim[openai,vertexai,logfire]"
```

**Note**: Specific model dependencies can be found in the models documentation.