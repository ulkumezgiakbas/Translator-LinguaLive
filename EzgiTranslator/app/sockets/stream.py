from __future__ import annotations
from flask import current_app
from flask_sock import Sock
from ..services.translate import translate_text

sock = Sock()


from flask import Flask  

def _init_sock(app: Flask):
    sock.init_app(app)


def _ensure_register():
    app = current_app._get_current_object() if current_app else None
   
_ensure_register()

@sock.route("/ws/translate")
def ws_translate(ws):
    
    while True:
        msg = ws.receive()
        if msg is None:
            break
        try:
            import json
            data = json.loads(msg)
            text = (data.get("text") or "").strip()
            src  = (data.get("source") or "auto").strip()
            tgt  = (data.get("target") or "en").strip()
            if not text:
                ws.send("")
                continue
            out = translate_text(text, source=src, target=tgt)
            ws.send(out)
        except Exception as e:
            ws.send(f"[ERR] {e}")
