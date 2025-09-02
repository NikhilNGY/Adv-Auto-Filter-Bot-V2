import os

# Helper to require environment variables
def _require(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value

# Required configs
BOT_TOKEN = _require("BOT_TOKEN")
API_ID = int(_require("API_ID"))
API_HASH = _require("API_HASH")
DATABASE_URL = _require("DATABASE_URL")

# Optional configs
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))  # 0 means disabled
ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split() if x]

# Defaults
RESULTS_COUNT = int(os.environ.get("RESULTS_COUNT", "5"))
