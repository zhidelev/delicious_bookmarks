FROM python:3.12-slim

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock

RUN pip install poetry --root-user-action=ignore && poetry install --no-root --no-directory 

COPY ./src/app /code/app

RUN poetry install --without dev,test

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]