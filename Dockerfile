FROM python:3.13-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
WORKDIR /app
RUN apk add --no-cache gcc musl-dev libffi-dev
COPY app.py .
COPY gallery.html.j2 .
RUN pip install --no-cache-dir Flask
EXPOSE 5000
CMD ["flask", "run"]
