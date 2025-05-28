FROM python:3.11-alpine AS builder

RUN apk add --no-cache build-base libffi-dev
WORKDIR /app
ENV VENV_PATH=/venv
RUN python -m venv $VENV_PATH
COPY requirements.txt .
RUN $VENV_PATH/bin/pip install --upgrade pip \
    && $VENV_PATH/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine

RUN apk add --no-cache libffi
COPY --from=builder /venv /venv
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /app
COPY app.py .
COPY gallery.html.j2 .
EXPOSE 5000
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "5000", "app:app"]
LABEL org.opencontainers.image.source=https://github.com/streambinder/serica
