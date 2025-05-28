import os
from typing import Optional

from flask import Flask, render_template, request, send_file

app = Flask(__name__, template_folder=os.getcwd())

TITLE = os.getenv("TITLE", "Gallery")
MEDIA_EXTENSIONS = (".jpg", ".jpeg", ".png", ".mp4", ".mov")


def get_galleries() -> list[str]:
    return [fdir for fdir in os.listdir("/data") if os.path.isdir(f"/data/{fdir}")]


def get_gallery_images(gallery: Optional[str] = None) -> list[str]:
    return [
        f"{gallery or ''}/{fname}"
        for fname in os.listdir(f"/data/{gallery or ''}")
        if fname.lower().endswith(MEDIA_EXTENSIONS) and fname != "cover.jpg"
    ]


def partition_media(media: list[str]) -> list[list[str]]:
    result = []
    i = 0
    pattern = [2, 2, 1]
    while i < len(media):
        for size in pattern:
            if i >= len(media):
                break
            group = media[i : i + size]
            result.append(group)
            i += size
    return result


@app.route("/media")
def media():
    return send_file(f"/data/{request.args.get('name')}", mimetype="image")


@app.route("/branding/<asset>")
def branding(asset: str):
    return send_file(f"/branding/{asset}", mimetype="image")


@app.route("/<gallery>")
def gallery(gallery: str):
    return render_template(
        "gallery.html.j2",
        galleries=get_galleries(),
        gallery_media=partition_media(get_gallery_images(gallery)),
        gallery_name=gallery,
        title=f"{gallery} — {TITLE}",
    )


@app.route("/")
def index():
    return render_template(
        "gallery.html.j2",
        galleries=get_galleries(),
        gallery_media=partition_media(get_gallery_images()),
        gallery_name="",
        title=TITLE,
    )
