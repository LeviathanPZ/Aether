# Charakter-Studio (18+)

Chat mit **gespeicherten Figuren**: Aussehen bleibt gleich, die Szene kommt aus dem Chat. Bilder erzeugt ein **lokales** Stable-Diffusion-WebUI (Forge / Automatic1111 / SD.Next), nicht GitHub und nicht ChatGPT.

**Nur fiktive Erwachsene (18+).** Keine Minderjährigen, nichts Altersunklares, keine realen Personen ohne Recht.

## Was dieses Repo ist

| Enthalten | Nicht enthalten |
|---|---|
| Chat-UI (Gradio) | Bildmodelle (mehrere GB) |
| Charakter-Speicher als JSON | fertige Erotik-Bilder |
| Prompt-Bau: Figur + Szene | Cloud-API, die NSFW oft blockt |
| Anbindung an lokales SD-WebUI | GPU bei GitHub |

GitHub speichert den **Code**. Die Bilder entstehen auf deinem Rechner.

## So bleibt die Person gleich

1. Figur einmal anlegen: Name, **Alter ≥ 18**, festes Aussehen (Haare, Augen, Gesicht, Körperbau).
2. Optional ein Referenzbild speichern.
3. Jede Chat-Szene hängt automatisch an diese Karte.
4. Ohne gespeicherte Karte würfelt das Modell jedes Mal ein neues Gesicht.

Für noch stabilere Gesichter später: IP-Adapter / InstantID / ein Character-LoRA im WebUI — die Textkarte reicht zum Start.

## Voraussetzungen

- Python 3.10+
- Optional für echte Bilder: [Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge) oder Automatic1111, GPU, ein Modell das du selbst wählst
- Im WebUI: **API aktivieren** (`--api`)

Viele Cloud-Bilddienste (DALL·E, ChatGPT-Bilder, Gemini) **blocken Erotik**. Deshalb ist die Schnittstelle lokal.

## Start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Browser: `http://127.0.0.1:7860` der App (Gradio). Das SD-WebUI läuft oft auf dem **gleichen** Port — dann in `.env` z. B. `SD_WEBUI_URL=http://127.0.0.1:7861` setzen und das WebUI auf einem anderen Port starten.

Ohne laufendes WebUI startet die App trotzdem: du siehst den gebauten Prompt (Figur bleibt gespeichert), es entsteht nur kein Bild.

## GitHub

Privates Repo empfohlen. Keine generierten Bilder, keine `.env`, keine Modelle committen (steht in `.gitignore`).

```bash
git init
git add .
git commit -m "Charakter-Studio: Chat, Speicher, lokale Bild-API"
git remote add origin git@github.com:DEINNAME/charakter-studio.git
git push -u origin main
```

Oben in der GitHub-Beschreibung: **18+ / fictional adults only**.

## Grenzen

- Textkarte: Kleidung und Haarfarbe oft gut, Gesicht über viele Szenen nur mittel.
- Referenzbild + IP-Adapter: deutlich besser.
- 100 % identisches Gesicht wie ein Foto-Double: meist nicht.
- Die App erzeugt nur, was dein **lokales Modell** erlaubt. Regeln und Gesetze bleiben bei dir.

## Dateien

- `app.py` — Chat-UI
- `characters.py` — Speichern / Laden / 18+-Prüfung
- `prompts.py` — Figur + Szene → Prompt
- `generate.py` — Aufruf SD-WebUI `txt2img`
- `data/characters/` — eine JSON-Datei pro Figur
