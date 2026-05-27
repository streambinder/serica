from __future__ import annotations

import os

from flask import Flask, abort, render_template, request, send_file
from flask.typing import ResponseReturnValue
from werkzeug.security import safe_join

app = Flask(__name__, template_folder=os.getcwd())

TITLE = os.getenv("TITLE", "Gallery")
DATA_DIR = "/data"
BRANDING_DIR = "/branding"
MEDIA_EXTENSIONS = (".jpg", ".jpeg", ".png", ".mp4", ".mov")
GRID_PATTERN = [2, 2, 1]


def get_galleries() -> list[str]:
    return [fdir for fdir in os.listdir(DATA_DIR) if os.path.isdir(f"{DATA_DIR}/{fdir}")]


def get_gallery_images(gallery_name: str | None = None) -> list[str]:
    # safe_join blocks .. traversal and absolute paths; None gallery_name = root
    gallery_dir = safe_join(DATA_DIR, gallery_name or "")
    if gallery_dir is None or not os.path.isdir(gallery_dir):
        return []
    return [
        f"{gallery_name or ''}/{fname}"
        for fname in os.listdir(gallery_dir)
        if fname.lower().endswith(MEDIA_EXTENSIONS) and fname != "cover.jpg"
    ]


def partition_grid(items: list[str]) -> list[list[str]]:
    i = 0
    result: list[list[str]] = []
    while i < len(items):
        for size in GRID_PATTERN:
            if i >= len(items):
                break
            group = items[i : i + size]
            result.append(group)
            i += size
    return result


@app.route("/health")
def health() -> ResponseReturnValue:
    return "OK", 200


@app.route("/media")
def media() -> ResponseReturnValue:
    name = request.args.get("name", "")
    path = safe_join(DATA_DIR, name)
    if path is None or not name.lower().endswith(MEDIA_EXTENSIONS) or not os.path.isfile(path):
        abort(404)
    return send_file(path)


@app.route("/branding/<path:asset>")
def branding(asset: str) -> ResponseReturnValue:
    path = safe_join(BRANDING_DIR, asset)
    if path is None or not os.path.isfile(path):
        abort(404)
    return send_file(path)


@app.route("/<gallery_name>")
def gallery(gallery_name: str) -> ResponseReturnValue:
    if safe_join(DATA_DIR, gallery_name) is None:
        abort(404)
    return render_template(
        "gallery.html.j2",
        galleries=get_galleries(),
        gallery_media=partition_grid(get_gallery_images(gallery_name)),
        gallery_name=gallery_name,
        title=f"{gallery_name} — {TITLE}",
    )


@app.route("/")
def index() -> ResponseReturnValue:
    return render_template(
        "gallery.html.j2",
        galleries=get_galleries(),
        gallery_media=partition_grid(get_gallery_images()),
        gallery_name="",
        title=TITLE,
    )
