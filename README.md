# Description
Simple example of a REST API implemented in FastAPI which provides pokemon stats using an LLM.

# Development setup
- **POETRY** for dependency management
- **RUFF**, **BLACK** and **ISORT** for formatting and linting
- **MYPY** for type checking
- **PRE-COMMIT** to automatically run the above tools before git commit

# Implementation
- Single API endpoint which accepts name or description of a pokemon and returns structured stats about the pokemon, if successfully identified
- Interchangable LLM Providers through DI - only OpenAI provider implemented
## Instructor
- Simple library which wraps LLM SDKs and implements easy enforcement of structured LLM output using Pydantic models
- Takes advantage of LLM models optimized for function calling and tool usage, since they are fine-tuned to output a JSON schema
- A production scenario would likely require a more sophisticated library or custom prompting and logic, but for a simple scenario such as this one, instructor works well enough, even on GPT-3.5-Turbo
- Relying on the LLM to provide the pokemon stat knowledge on each call is not optimal - in a production scenario it woudld be preferrable to aggregate the pokemon data beforehand, only use the LLM to identify the pokemon name from user query and then retrieve the pokemon stats from a static knowledge base

# Containerization
- The app is meant to be run in Docker
- The Dockerfile usses a multi-stage build process, to avoid installing unnecessary dependencies (such as Poetry) in the final image (this is one disadvantage of Poetry - especially for simple apps it results in a more complicated Dockerfile than the standard PIP and requirements.txt approach)
  - base stage for common setup
  - builder stage for installing dependencies
  - runner stage for the final image (installed dependencies are copied from builder stage)

To build and run the container locally:
```bash
docker build -t app . && docker run --env-file .env -p 8000:8000 app
```

# Testing
## Unit tests
- Using **PYTEST**
- Test the API endpoint handling in isolation (using a mock LLM provider)
- Test the implemented OpenAI provider in isolation (using a mock SDK function)

Can be run locally:
```bash
poetry run pytest tests/unit/
```
or in a testing Docker container:
```bash
docker build -f Dockerfile.unit-tests -t unit-tests . && docker run --env-file .env --rm unit-tests
```

## Integration (end-to-end) tests
- Using **PYTEST** and docker-compose (the app container and a test container which sends http requests to the API)
- Test the API and its containerization, as well as a specific LLM provider on example queries

Can be run with docker-compose:
```bash
docker-compose -f docker-compose.integration-tests.yml up --build
```

# Logging
- Basically the default logging config I use whenever starting a new python repo - not very useful in a containerized application. In a production scenario, there would be a real logging handler integrated.
  - HTTPException middleware
  - correlation id middleware for tracing
  - json formatter for log files
