from __future__ import annotations
from flask import Blueprint, render_template, request, jsonify
from ..services.translate import translate_text, SUPPORTED

bp = Blueprint("ui", __name__)

@bp.get("/")
def index():
    return render_template("index.html", supported=SUPPORTED)

@bp.post("/api/translate")
def api_translate():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    src = (data.get("source") or "auto").strip()
    tgt = (data.get("target") or "en").strip()
    if not text:
        return jsonify({"text": "", "source": src, "target": tgt}), 200
    out = translate_text(text, source=src, target=tgt)
    return jsonify({"text": out, "source": src, "target": tgt})
