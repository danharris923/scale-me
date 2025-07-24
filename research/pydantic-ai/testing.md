# Pydantic AI Testing Guide

## Overview
Comprehensive guide to unit testing Pydantic AI agents without making real LLM calls.

## Testing Strategies
- Use `pytest` as the test harness
- Utilize `inline-snapshot` and `dirty-equals` for complex assertions
- Use `TestModel` or `FunctionModel` to avoid real LLM calls
- Use `Agent.override` to replace models, dependencies, or toolsets
- Set `ALLOW_MODEL_REQUESTS=False` to prevent accidental model requests

## Key Testing Approaches

### 1. TestModel Testing
- Generates basic structured data based on tool schemas
- Fastest way to exercise application code
- Doesn't use actual ML/AI logic
- Generates procedural Python data satisfying JSON schemas

```python
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

agent = Agent('test')  # Uses TestModel by default in tests

async def test_basic_response():
    result = await agent.run('Tell me a joke')
    assert isinstance(result.output, str)
```

### 2. FunctionModel Testing
- Allows custom input and response generation
- More flexible than TestModel
- Can simulate specific tool interactions
- Enables detailed testing of tool behaviors

```python
from pydantic_ai.models.function import FunctionModel

def custom_response_func(messages):
    # Custom logic to generate responses based on input
    return "Custom response"

agent = Agent(FunctionModel(custom_response_func))
```

## Example Testing Techniques
- Use `capture_run_messages()` to inspect agent-model interactions
- Override models using pytest fixtures
- Test async functions with `anyio`
- Validate tool calls, responses, and database interactions

## Key Testing Tools
- `TestModel`: Generates basic structured responses
- `FunctionModel`: Enables custom response generation
- `Agent.override()`: Replace model components during testing
- `capture_run_messages()`: Inspect agent interactions

## Testing Best Practices
```python
import pytest
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

@pytest.fixture
def test_agent():
    agent = Agent('openai:gpt-4o')
    return agent.override(model=TestModel())

async def test_agent_with_tools(test_agent):
    # Test with overridden model
    result = await test_agent.run('Calculate 2+2')
    assert result.output is not None
```

## Environment Variables for Testing
```python
# Prevent accidental API calls
import os
os.environ['ALLOW_MODEL_REQUESTS'] = 'False'
```

The guide emphasizes creating comprehensive, controlled tests that simulate agent behaviors without making actual LLM calls, ensuring fast and reliable test execution.