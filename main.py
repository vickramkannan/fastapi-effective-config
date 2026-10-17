import os
from pathlib import Path

import yaml
from dotenv import dotenv_values
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULTS = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}


def coerce(key, value):
    if key in ("port", "workers"):
        return int(value)
    if key == "debug":
        return str(value).strip().lower() in ("true", "1", "yes", "on")
    return str(value)


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    config = DEFAULTS.copy()

    env_name = os.getenv("APP_ENV", "development")
    yaml_path = Path(f"config.{env_name}.yaml")
    if yaml_path.exists():
        with yaml_path.open(encoding="utf-8") as f:
            config.update(yaml.safe_load(f) or {})

    for key, value in dotenv_values(".env").items():
        if value is None:
            continue
        normalized = key.lower()
        if normalized == "num_workers":
            normalized = "workers"
        config[normalized] = value

    for key, value in os.environ.items():
        if key.startswith("APP_") and key != "APP_ENV":
            normalized = key[4:].lower()
            if normalized:
                config[normalized] = value

    for item in set:
        if "=" in item:
            key, value = item.split("=", 1)
            config[key.strip().lower()] = value

    result = {key: coerce(key, value) for key, value in config.items()}
    result["api_key"] = "****"
    return result
