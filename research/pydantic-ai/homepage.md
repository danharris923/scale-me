# Pydantic AI Homepage Documentation

Pydantic AI Overview:
- An agent framework for building production-grade generative AI applications in Python
- Created by the Pydantic team to bring "FastAPI feeling" to GenAI development

Key Features:
- Model-agnostic support (OpenAI, Anthropic, Gemini, etc.)
- Integrated with Pydantic Logfire for debugging
- Type-safe design
- Structured response validation
- Dependency injection system
- Streamed response capabilities
- Graph support

Core Strengths:
- Built by Pydantic Validation team
- Supports multiple AI models
- Emphasizes Python-centric design
- Enables type checking and structured outputs

Code Example (Hello World):
```python
from pydantic_ai import Agent
agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt='Be concise, reply with one sentence.'
)
result = agent.run_sync('Where does "hello world" come from?')
print(result.output)
```

Documentation Sections:
- Installation
- Getting Help
- Contributing
- Troubleshooting
- Upgrade Guide
- Detailed documentation on:
  - Agents
  - Models
  - Dependencies
  - Tools
  - Output handling
  - Testing
  - Multi-agent applications

Comprehensive Examples Available:
- Agent User Interaction
- Weather Agent
- Bank Support
- SQL Generation
- Flight Booking
- RAG (Retrieval-Augmented Generation)

Next Steps:
- Explore examples
- Read documentation
- Review API Reference

The documentation provides a robust framework for developers looking to build AI-powered applications with strong typing and structured outputs.