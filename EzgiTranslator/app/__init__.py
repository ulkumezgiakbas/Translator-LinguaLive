from __future__ import annotations
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        JSON_AS_ASCII=False,
        JSON_SORT_KEYS=False,
        SECRET_KEY="dev",   
        TRANSLATE_PROVIDER="libre",  
        LIBRE_URL="https://libretranslate.com/translate",  
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    )

    from .blueprints.ui import bp as ui_bp
    app.register_blueprint(ui_bp)

    from .sockets.stream import sock  

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  

    @app.after_request
    def _headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("Referrer-Policy", "no-referrer")
        return resp

    return app
