# Pydantic AI Dependencies Documentation

## Overview
Dependencies in Pydantic AI are a system for providing data and services to agents, tools, and output validators. They're designed to use Python best practices for type-safe, understandable dependency management.

## Key Characteristics
- Can be any Python type, but dataclasses are recommended for multiple objects
- Accessed through `RunContext`
- Support both synchronous and asynchronous dependencies

## Defining Dependencies
```python
from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient

agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps
)
```

## Accessing Dependencies
```python
@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get('https://example.com')
    return f'Prompt: {response.text}'

@agent.tool
async def fetch_data(ctx: RunContext[MyDeps], url: str) -> str:
    response = await ctx.deps.http_client.get(url)
    return response.text
```

## Key Features
- Can be used in system prompts, tools, and output validators
- Supports runtime dependency overriding for testing
- Works with both synchronous and asynchronous methods

## Dependency Overriding (for Testing)
```python
class TestMyDeps(MyDeps):
    async def system_prompt_factory(self) -> str:
        return 'test prompt'

# Override dependencies during testing
with agent.override(deps=test_deps):
    result = await agent.run('Tell me a joke.')
```

## Best Practices
- Prefer async methods for IO-heavy dependencies
- Use dataclasses to organize complex dependencies
- Leverage type checking for dependency management
- Keep dependencies focused and single-purpose

## Example Use Cases
- Weather Agent: Passing API keys and HTTP clients
- SQL Generation: Passing database connections
- Retrieval-Augmented Generation (RAG): Passing vector stores and embeddings

The dependency system aims to make dependencies "type-safe, understandable, easier to test and ultimately easier to deploy in production."