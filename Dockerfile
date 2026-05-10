FROM ghcr.io/astral-sh/uv:0.11.12 AS uv

FROM python:3.14-alpine AS builder
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

FROM python:3.14-alpine
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY app.py gallery.html.j2 ./
EXPOSE 5000
USER nobody
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --spider --quiet http://127.0.0.1:5000/health || exit 1
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "5000", "app:app"]
LABEL org.opencontainers.image.source=https://github.com/streambinder/serica
