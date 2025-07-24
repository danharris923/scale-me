# Pydantic AI Model Providers Documentation

Supported Model Providers:
- OpenAI
- Anthropic
- Gemini (via Generative Language API and VertexAI)
- Groq
- Mistral
- Cohere
- Bedrock
- Hugging Face

OpenAI-Compatible Providers:
- DeepSeek
- Grok (xAI)
- Ollama
- OpenRouter
- Perplexity
- Fireworks AI
- Together AI
- Azure AI Foundry
- Heroku
- GitHub Models

Key Concepts:
1. "Model": Pydantic AI class for making requests to specific LLM APIs
2. "Provider": Handles authentication and connections to LLM vendors
3. "Profile": Describes how to construct requests for optimal results

Custom Model Implementation:
- Subclass the `Model` abstract base class
- Implement `StreamedResponse` for streaming
- Review existing implementations like `OpenAIModel`

Fallback Model Feature:
- Use `FallbackModel` to attempt multiple models sequentially
- Automatically switches models on 4xx/5xx status codes
- Can configure individual model settings

Example of Fallback Model:
```python
fallback_model = FallbackModel(openai_model, anthropic_model)
agent = Agent(fallback_model)
response = agent.run_sync('Question')
```

Configuration Tips:
- Set `base_url`, `api_key`, and custom clients individually for each model
- Use `ModelSettings` to configure temperature, max tokens, etc.

The documentation emphasizes model-agnostic design, allowing easy switching between different AI providers with minimal code changes.