from characters import validate_character

NEGATIVE = (
    "child, children, kid, kids, minor, underage, teen, teenager, loli, shota, "
    "young, baby, infant, school uniform, childlike, preteen, "
    "minderjährig, kind, kinder, jugendlich, "
    "deformed, extra fingers, extra limbs, blurry, watermark, text, logo, "
    "inconsistent face, different person, identity change"
)


def build_prompts(character: dict, scene: str) -> tuple[str, str]:
    error = validate_character(character)
    if error:
        raise ValueError(error)

    scene = (scene or "").strip()
    if not scene:
        raise ValueError("Szene / Chat-Text fehlt.")

    identity = (
        f"same character always, consistent identity, consistent face, "
        f"named {character['name']}, adult, {character['age']} years old, "
        f"{character['appearance']}"
    )
    if character.get("clothing"):
        identity += f", typically {character['clothing']}"

    style = character.get("style") or "photorealistic, cinematic lighting"
    prompt = f"{identity}, {scene}, {style}"
    return prompt, NEGATIVE
