import json
import re
import unicodedata
from pathlib import Path

from config import BLOCKED_TERMS, CHAR_DIR, MIN_AGE, REF_DIR


def _slug(name: str) -> str:
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "charakter"


def _collect_text(character: dict) -> str:
    parts = [
        character.get("name", ""),
        character.get("appearance", ""),
        character.get("clothing", ""),
        character.get("style", ""),
        str(character.get("notes", "")),
    ]
    return " ".join(parts).lower()


def validate_character(character: dict) -> str | None:
    name = (character.get("name") or "").strip()
    if not name:
        return "Name fehlt."

    try:
        age = int(character.get("age"))
    except (TypeError, ValueError):
        return "Alter muss eine Zahl sein."

    if age < MIN_AGE:
        return f"Nur fiktive Erwachsene ({MIN_AGE}+). Alter {age} ist nicht erlaubt."

    if not (character.get("appearance") or "").strip():
        return "Aussehen fehlt. Ohne feste Beschreibung ändert sich das Gesicht."

    blob = _collect_text(character)
    for term in BLOCKED_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", blob, flags=re.IGNORECASE):
            return f"Ungültiger Begriff in der Charakterkarte: «{term}». Nur Erwachsene."

    return None


def character_path(char_id: str) -> Path:
    return CHAR_DIR / f"{char_id}.json"


def list_characters() -> list[dict]:
    items = []
    for path in sorted(CHAR_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data["id"] = path.stem
            items.append(data)
        except (OSError, json.JSONDecodeError):
            continue
    return items


def load_character(char_id: str) -> dict | None:
    path = character_path(char_id)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    data["id"] = path.stem
    return data


def save_character(character: dict, reference_path: str | None = None) -> dict:
    error = validate_character(character)
    if error:
        raise ValueError(error)

    char_id = character.get("id") or _slug(character["name"])
    character = {
        "id": char_id,
        "name": character["name"].strip(),
        "age": int(character["age"]),
        "appearance": character["appearance"].strip(),
        "clothing": (character.get("clothing") or "").strip(),
        "style": (character.get("style") or "fotorealistisch, weiches Licht, konsistentes Gesicht").strip(),
        "notes": (character.get("notes") or "").strip(),
        "reference_image": character.get("reference_image") or "",
    }

    if reference_path:
        src = Path(reference_path)
        if src.exists():
            dest = REF_DIR / f"{char_id}{src.suffix.lower() or '.png'}"
            dest.write_bytes(src.read_bytes())
            character["reference_image"] = str(dest)

    character_path(char_id).write_text(
        json.dumps(character, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return character


def delete_character(char_id: str) -> None:
    path = character_path(char_id)
    if path.exists():
        path.unlink()


def character_choices() -> list[str]:
    return [f"{c['name']} ({c['age']}) [{c['id']}]" for c in list_characters()]


def id_from_choice(choice: str) -> str | None:
    if not choice or "[" not in choice:
        return None
    return choice.rsplit("[", 1)[-1].rstrip("]")
