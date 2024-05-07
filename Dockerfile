FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN python -m pip install --upgrade pip
RUN pip install poetry && poetry install --no-interaction --no-ansi
COPY . .
EXPOSE 8080
CMD ["poetry", "run", "python", "app.py"]