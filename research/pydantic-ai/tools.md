# Pydantic AI Function Tools Documentation

Function Tools Overview
----------------------

Function tools are mechanisms that allow AI models to:
- Perform actions
- Retrieve additional information
- Enhance response generation
- Make agent behavior more deterministic

Key Tool Registration Methods:
1. `@agent.tool` decorator (recommended, provides agent context)
2. `@agent.tool_plain` decorator (for tools without context)
3. Tools passed via Agent constructor argument

Tool Creation Principles
-----------------------

### Basic Tool Example
```python
@agent.tool_plain
def roll_dice() -> str:
    """Roll a six-sided die and return the result."""
    return str(random.randint(1, 6))
```

### Context-Aware Tool
```python
@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps
```

Tool Schema and Validation
-------------------------

- Parameters extracted from function signatures
- Docstring descriptions automatically added to tool schema
- Supports Google, NumPy, and Sphinx docstring formats
- Automatic parameter validation using Pydantic

### Custom Schema Example
```python
tool = Tool.from_schema(
    function=foobar,
    name='sum',
    description='Sum two numbers.',
    json_schema={
        'properties': {
            'a': {'description': 'first number', 'type': 'integer'},
            'b': {'description': 'second number', 'type': 'integer'}
        }
    }
)
```

Dynamic Tools
-------------

Tools can have:
- Per-tool `prepare` methods
- Agent-wide `prepare_tools` function

These allow dynamic:
- Tool enabling/disabling
- Tool definition modification
- Conditional tool registration

Retry Mechanisms
----------------

Two primary retry scenarios:
1. Validation errors (automatic)
2. Manual retries via `ModelRetry` exception

```python
def my_flaky_tool(query: str) -> str:
    if query == 'bad':
        raise ModelRetry("Invalid query. Try again.")
    return 'Success!'
```