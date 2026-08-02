# Nightjar

Nightjar is a RBAC system named after the bird. https://en.wikipedia.org/wiki/Nightjar

# Tech stack:
- Python
- FastAPI
- PostgreSQL
- Testing with Postman, Swagger, or Bruno

Feature list is in the GitHub project


# Development:

For this project we are using 'uv' instead of pip.  If you are just getting
started with this project:

- git clone
- uv sync
- uv run uvicorn src.api:app --reload

If you need to add a dependency to the project:
- uv add "module_name"

If you are revisiting the project and are missing dependencies:
- uv sync
