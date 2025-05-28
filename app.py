import os
from typing import Optional

from flask import Flask, render_template, request, send_file

app = Flask(__name__, template_folder=os.getcwd())

TITLE = os.getenv("TITLE", "Gallery")
MEDIA_EXTENSIONS = (".jpg", ".jpeg", ".png", ".mp4", ".mov")
GRID_PATTERN = [2, 2, 1]


def get_galleries() -> list[str]:
    return [fdir for fdir in os.listdir("/data") if os.path.isdir(f"/data/{fdir}")]


def get_gallery_images(gallery_name: Optional[str] = None) -> list[str]:
    return [
        f"{gallery_name or ''}/{fname}"
        for fname in os.listdir(f"/data/{gallery_name or ''}")
        if fname.lower().endswith(MEDIA_EXTENSIONS) and fname != "cover.jpg"
    ]


def partition_grid(items: list[str]) -> list[list[str]]:
    i = 0
    result = []
    while i < len(items):
        for size in GRID_PATTERN:
            if i >= len(items):
                break
            group = items[i : i + size]
            result.append(group)
            i += size
    return result


@app.route("/health")
def health():
    return "OK", 200


@app.route("/media")
def media():
    return send_file(f"/data/{request.args.get('name')}", mimetype="image")


@app.route("/branding/<asset>")
def branding(asset: str):
    return send_file(f"/branding/{asset}", mimetype="image")


@app.route("/<gallery_name>")
def gallery(gallery_name: str):
    return render_template(
        "gallery.html.j2",
        galleries=get_galleries(),
        gallery_media=partition_grid(get_gallery_images(gallery_name)),
        gallery_name=gallery_name,
        title=f"{gallery_name} — {TITLE}",
    )


@app.route("/")
def index():
    return render_template(
        "gallery.html.j2",
        galleries=get_galleries(),
        gallery_media=partition_grid(get_gallery_images()),
        gallery_name="",
        title=TITLE,
    )
