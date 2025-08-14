from __future__ import annotations
import os
import requests
from flask import current_app


SUPPORTED = [
    ("auto", "Auto Detect"),
    ("en", "English"),
    ("tr", "Turkish"),
    ("es", "Spanish"),
    ("de", "German"),
    ("fr", "French"),
    ("it", "Italian"),
    ("pt", "Portuguese"),
    ("ru", "Russian"),
    ("ar", "Arabic"),
    ("zh", "Chinese"),
    ("ja", "Japanese"),
    ("ko", "Korean"),
]


LT_FALLBACKS = [

    "https://libretranslate.de/translate",
    "https://translate.argosopentech.com/translate",
    "https://libretranslate.com/translate",
]

UA_HEADERS = {
    "User-Agent": "LinguaLive/1.0 (+local dev)",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def translate_text(text: str, source: str = "auto", target: str = "en") -> str:
    

    try:
        out = _libretranslate_multi(text, source=source, target=target)
        if out:
            return out
    except Exception:
        pass


    try:
        return _mymemory(text, source=source, target=target)
    except Exception as e:
        raise RuntimeError(f"All translators failed: {e}")

def _libretranslate_multi(text: str, source: str, target: str) -> str:
    url_cfg = (current_app.config.get("LIBRE_URL") or "").strip()
    candidates = []
    if url_cfg:
        candidates.append(url_cfg)
    candidates.extend([u for u in LT_FALLBACKS if u != url_cfg])

    last_err = None
    for url in candidates:
        try:
            payload = {"q": text, "source": source, "target": target, "format": "text"}
            r = requests.post(url, json=payload, headers=UA_HEADERS, timeout=20)
            if r.status_code >= 400:
                last_err = RuntimeError(f"LibreTranslate {url} -> {r.status_code}: {r.text[:120]}")
                continue
            data = r.json()
            out = data.get("translatedText", "")
            if out:
                return out
        except Exception as e:
            last_err = e
            continue
    if last_err:
        raise last_err
    return ""

def _mymemory(text: str, source: str, target: str) -> str:
    """
    MyMemory ücretsiz API (oran/limit var). Auto detect desteklemez;
    'auto' gelirse basitçe 'en' varsayıyoruz.
    """
    src = source if source != "auto" else "en"

    params = {
        "q": text,
        "langpair": f"{src}|{target}",
    }
    r = requests.get("https://api.mymemory.translated.net/get", params=params, headers={"User-Agent": UA_HEADERS["User-Agent"]}, timeout=20)
    r.raise_for_status()
    data = r.json() or {}
    resp = (data.get("responseData") or {}).get("translatedText", "")
    return resp or ""
