FROM python:3.10-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.13.8@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 /uv /uvx /usr/local/bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_TOOL_DIR=/opt/uv-tools \
    UV_TOOL_BIN_DIR=/usr/local/bin

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY setup.py pyproject.toml README.md LICENSE package.json requirements-test.txt requirements-container.txt /app/
COPY pokemonterminal /app/pokemonterminal

# Update the base image's provisioning tools; do not remove them from the scan.
RUN uv pip install --system --upgrade -r requirements-container.txt

# Install the app with the documented installer; keep all provisioning tools.
RUN uv tool install --python 3.10 . \
    && uv pip freeze --python /opt/uv-tools/pokemon-terminal/bin/python --exclude pokemon-terminal > /tmp/runtime-requirements.txt \
    && uv pip install --python /opt/uv-tools/pokemon-terminal/bin/python --constraint /tmp/runtime-requirements.txt -r requirements-test.txt

WORKDIR /checks
COPY tests /checks/tests
CMD ["/opt/uv-tools/pokemon-terminal/bin/python", "-m", "pytest", "tests", "-q"]
