FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY setup.py README.md LICENSE package.json /app/
COPY pokemonterminal /app/pokemonterminal
COPY tests /app/tests

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e . pytest

CMD ["pytest", "-q"]
