from __future__ import annotations

import json

import requests


def format_manifest(d: dict):
    formatted = {}
    for k, v in d.items():
        if k.startswith("@"):
            k = k.replace("@", "")  # for now, just remove the @
            formatted.setdefault("_at_fields", []).append(k)
        if k.startswith("_"):
            k = k.replace("_", "")  # for now, just remove the _
            formatted.setdefault("_underscore_fields", []).append(k)
        formatted[k] = v
    return formatted


def get_manifest(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.text, object_hook=format_manifest)
