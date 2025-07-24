# Pydantic AI Agent API Reference

## Agent Creation and Initialization

```python
from pydantic_ai import Agent

# Basic agent creation
agent = Agent('openai:gpt-4o')

# Advanced agent creation with options
agent = Agent(
    model='openai:gpt-4o',                    # Model identifier
    output_type=str,                          # Default output type
    instructions='Be helpful and concise',    # Base instructions
    deps_type=None,                          # Dependency type
    name='MyAgent',                          # Agent name
    model_settings=None,                     # Model-specific settings
    tools=[...],                             # Optional tools
    system_prompt='You are an AI assistant'  # System prompt
)
```

## Key Methods

### 1. Synchronous Run
```python
result = agent.run_sync('What is the capital of France?')
print(result.output)  # Prints: Paris
print(result.cost)    # Token usage cost
```

### 2. Asynchronous Run
```python
result = await agent.run('What is the capital of France?')
print(result.output)  # Prints: Paris
print(result.messages)  # List of messages exchanged
```

### 3. Streaming Run
```python
async with agent.run_stream('Tell me a story') as response:
    # Stream partial responses
    async for chunk in response.stream():
        print(chunk, end='')
    
    # Get final output
    output = await response.get_output()
```

## Decorators

### 1. Tool Registration
```python
@agent.tool
def calculate(ctx, x: int, y: int) -> int:
    """Perform addition of two numbers"""
    return x + y

@agent.tool_plain
def simple_tool() -> str:
    """Tool without context access"""
    return "Hello"
```

### 2. Instructions and System Prompts
```python
@agent.instructions
def get_instructions(ctx: RunContext) -> str:
    """Dynamic instructions based on context"""
    return "Be helpful and concise"

@agent.system_prompt
def system_context() -> str:
    """Define system behavior"""
    return "You are an AI assistant specialized in Python"
```

### 3. Output Validation
```python
from pydantic_ai import ModelRetry

@agent.output_validator
def validate_output(data: str) -> str:
    """Validate and optionally retry model output"""
    if len(data) > 100:
        raise ModelRetry('Output too long, please be more concise')
    return data
```

## Advanced Features

### Dependency Injection
```python
from dataclasses import dataclass

@dataclass
class Dependencies:
    db_connection: Database
    api_key: str

agent = Agent('openai:gpt-4o', deps_type=Dependencies)

# Use dependencies in tools
@agent.tool
async def fetch_user(ctx: RunContext[Dependencies], user_id: int):
    return await ctx.deps.db_connection.get_user(user_id)
```

### Custom Model Settings
```python
agent = Agent(
    'openai:gpt-4o',
    model_settings={
        'temperature': 0.7,
        'max_tokens': 1000
    }
)
```

### Multi-step Conversations
```python
# Continue a conversation
result1 = await agent.run('What is Python?')
result2 = await agent.run(
    'Can you give me an example?',
    message_history=result1.messages
)
```

### Tool Preparation
```python
# Prepare tools before execution
@agent.tool
async def search(ctx: RunContext, query: str) -> str:
    # Tool implementation
    pass

# Tools can access context and return results
```

### Model Override
```python
# Override model for testing or different scenarios
with agent.override(model='anthropic:claude-3'):
    result = await agent.run('Hello')
```

## Complete Example
```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from dataclasses import dataclass

class OutputSchema(BaseModel):
    summary: str
    confidence: float

@dataclass
class MyDeps:
    api_key: str

agent = Agent(
    'openai:gpt-4o',
    output_type=OutputSchema,
    deps_type=MyDeps
)

@agent.system_prompt
def system_prompt() -> str:
    return "You are a helpful assistant that provides summaries with confidence scores."

@agent.tool
async def web_search(ctx: RunContext[MyDeps], query: str) -> str:
    # Perform web search using API key from dependencies
    return f"Search results for: {query}"

# Run the agent
deps = MyDeps(api_key="your-api-key")
result = await agent.run(
    "Summarize the latest AI news",
    deps=deps
)
print(f"Summary: {result.output.summary}")
print(f"Confidence: {result.output.confidence}")
```