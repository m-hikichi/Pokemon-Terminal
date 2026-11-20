FROM alpine:3.23
COPY --from=ghcr.io/astral-sh/uv:0.13.8@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 /uv /uvx /usr/local/bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_TOOL_DIR=/opt/uv-tools \
    UV_TOOL_BIN_DIR=/usr/local/bin

# 通常利用と同じuvによる導入に合わせ、Alpine公式のPython 3.12を使用する。
# パッケージの導入はuvで行うため、別パッケージのpy3-pipは追加しない。
RUN apk upgrade --no-cache \
    && apk add --no-cache ca-certificates 'python3~3.12' \
    && python3 -c 'import sys; assert sys.version_info[:2] == (3, 12), sys.version'

WORKDIR /app
COPY setup.py pyproject.toml README.md LICENSE package.json requirements-test.txt /app/
COPY pokemonterminal /app/pokemonterminal

RUN uv tool install --python 3.12 . \
    && uv pip freeze --python /opt/uv-tools/pokemon-terminal/bin/python --exclude pokemon-terminal > /tmp/runtime-requirements.txt \
    && uv pip install --python /opt/uv-tools/pokemon-terminal/bin/python --constraint /tmp/runtime-requirements.txt -r requirements-test.txt

WORKDIR /checks
COPY tests /checks/tests
COPY scripts /checks/scripts
CMD ["/opt/uv-tools/pokemon-terminal/bin/python", "-m", "pytest", "tests", "-q"]
