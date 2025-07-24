# Pydantic AI Agents Documentation

Agents Overview
---------------

Agents are the primary interface for interacting with Large Language Models (LLMs) in Pydantic AI. They are designed to be:
- Reusable across applications
- Configurable with system prompts, tools, and output types
- Type-safe and compatible with static type checking

Key Agent Components:
1. System Prompts
2. Function Tools
3. Structured Output Type
4. Dependency Type Constraints
5. LLM Model
6. Model Settings

Basic Agent Creation Example:
```python
from pydantic_ai import Agent

agent = Agent(
    'openai:gpt-4o',  # Model selection
    deps_type=int,    # Dependency type
    output_type=bool, # Output type
    system_prompt='Instructions for the agent'
)
```

Agent Execution Methods
----------------------

Agents can be run in multiple ways:
1. `agent.run()` - Async coroutine returning full response
2. `agent.run_sync()` - Synchronous method returning response
3. `agent.run_stream()` - Async streaming response
4. `agent.iter()` - Detailed graph iteration

System Prompts and Instructions
-------------------------------

Two key configuration methods:

1. System Prompts:
- Preserved across message history
- Can be static or dynamic
- Useful for maintaining conversation context

2. Instructions:
- Reset with each new agent run
- Recommended default approach
- Can be static or dynamically generated

Example:
```python
agent = Agent(
    'openai:gpt-4o',
    instructions="Use the customer's name while replying",
    system_prompt="Retain conversation history"
)
```

Tools and Dependencies
---------------------

Agents can include function tools that:
- Extend model capabilities
- Provide external data/functionality
- Support retry mechanisms
- Are type-checked

Example:
```python
@agent.tool
def weather_forecast(location: str, date: date) -> str:
    # Tool implementation
    return forecast_data
```

Advanced Features
-----------------

- Type-safe design
- Structured response validation
- Dependency injection
- Streaming support
- Graph-based execution