import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
CHAR_DIR = DATA_DIR / "characters"
REF_DIR = DATA_DIR / "refs"
OUT_DIR = ROOT / "outputs"

for folder in (CHAR_DIR, REF_DIR, OUT_DIR):
    folder.mkdir(parents=True, exist_ok=True)

SD_WEBUI_URL = os.getenv("SD_WEBUI_URL", "http://127.0.0.1:7860").rstrip("/")
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "768"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "1024"))
STEPS = int(os.getenv("STEPS", "28"))
CFG_SCALE = float(os.getenv("CFG_SCALE", "7"))

MIN_AGE = 18

BLOCKED_TERMS = (
    "child",
    "children",
    "kid",
    "kids",
    "minor",
    "underage",
    "under-age",
    "loli",
    "shota",
    "preteen",
    "teen",
    "teenager",
    "schoolgirl",
    "schoolboy",
    "minderjährig",
    "minderjaehrig",
    "kinder",
    "kindlich",
    "jugendlich",
    "teenagerin",
    "schulmädchen",
    "schulmadchen",
    "schuljunge",
)
