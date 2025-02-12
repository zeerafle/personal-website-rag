FROM python:3.12.8-slim

RUN pip install uv

WORKDIR /app
COPY requirements.lock ./
RUN uv pip install --no-cache --system -r requirements.lock

COPY src ./src
COPY vector_store ./vector_store
COPY .env .
CMD ENV=production fastapi run src/personal_website_rag
