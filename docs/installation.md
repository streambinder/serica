# Installation

## Docker

The recommended way to run Serica is via Docker, pulling the prebuilt image from GHCR:

```bash
docker pull ghcr.io/streambinder/serica:latest
```

The published image targets `linux/arm64` only. On other architectures, build locally from the `Dockerfile` shipped at the repository root.

Mount your media directory at `/data` and your branding assets (logo, favicon) at `/branding`:

```bash
docker run -d \
  --name serica \
  -p 5000:5000 \
  -v /path/to/photos:/data:ro \
  -v /path/to/branding:/branding:ro \
  -e TITLE="My Gallery" \
  ghcr.io/streambinder/serica:latest
```

The container runs as `nobody` and exposes port 5000, with a healthcheck pinging `/health` every 30 seconds.

## Directory layout

Serica expects the following layout under the volumes:

```text
/data/
  trip-iceland/
    cover.jpg
    IMG_001.jpg
    IMG_002.jpg
    clip.mp4
  wedding/
    cover.jpg
    photo-001.png
    photo-002.png

/branding/
  logo.png
  favicon.png
```

Each subdirectory under `/data` becomes one gallery page reachable at `/<gallery-name>`. The optional `cover.jpg` inside a gallery is used as that gallery's hero image; if missing, the gallery still renders. Files with extensions outside `.jpg`, `.jpeg`, `.png`, `.mp4`, `.mov` are ignored.

Serica fetches `logo.png` and `favicon.png` from `/branding`. Both are required for the template to render correctly.

## Configuration

Serica reads its configuration from a single environment variable:

| Variable | Required | Default     | Purpose                                                       |
| -------- | -------- | ----------- | ------------------------------------------------------------- |
| `TITLE`  | no       | `"Gallery"` | Site title shown on the homepage cover and in the page titles |

## Custom build

Serica is a single-file Flask app, so the usual Python toolchain works:

```bash
git clone https://github.com/streambinder/serica.git
cd serica
uv sync --frozen
uv run waitress-serve --host 0.0.0.0 --port 5000 app:app
```

Note: the app hard-codes `/data` and `/branding` as absolute paths. To run outside Docker, create those directories at the filesystem root (or patch `DATA_DIR` and `BRANDING_DIR` in `app.py`).
