# 🌿 Plant Identification Glasses

**Lorenzo Morrison · Nick Croft · Rujuta Asanikar** — Algorithm Design

Smart glasses that identify plants in real time using computer vision, voice commands, and audio feedback — completely hands-free.

---

## Overview

Most AI image-recognition apps are clunky: open your phone, launch the app, point it, wait. This project cuts all of that out. By pairing smart glasses with a camera and the Plant.id API, you can identify any plant you're looking at simply by saying a voice command — and hear the result spoken back to you in under 10 seconds.

The glasses project is a proof of concept for a broader vision: smart glasses as a general-purpose AI assistant. Plant identification is just the starting point.

---

## How It Works

```
[Voice command via Siri/Shortcuts]
        ↓
[Automator app triggers Python script]
        ↓
[USB camera captures image]
        ↓
[Image sent to Plant.id API]
        ↓
[Result spoken back via TTS through glasses speakers]
```

1. User says **"Hey Siri, run Identify Plant"**
2. Siri triggers an Automator `.app` wrapper
3. The script captures a frame from the attached USB camera
4. The image is base64-encoded and sent to the [Plant.id API](https://plant.id/)
5. The top identification result (with confidence %) is read aloud via `pyttsx3` through the glasses' built-in speakers

---

## Hardware

| Component | Details |
|---|---|
| Smart glasses | OhO Sunshine (built-in mic + speakers) |
| External camera | Walfront Pro USB camera |
| Computer | macOS (runs the Python script locally) |

> **Note:** This is a prototype. The original plan was to use MentraLive glasses (which have a built-in camera), but they didn't arrive in time. The external camera is a temporary workaround — once MentraLive glasses are available, the setup becomes fully self-contained.

---

## Setup

### Prerequisites

- macOS
- Python 3.11 (via Homebrew: `/opt/homebrew/bin/python3.11`)
- [`imagesnap`](https://github.com/rharder/imagesnap) for camera capture

```bash
brew install imagesnap
```

### Install Python dependencies

```bash
pip3 install pillow pyttsx3 requests
```

### API Key

Get a free API key from [Plant.id](https://plant.id/) and set it in `identify_once.py`:

```python
API_KEY = "your_api_key_here"
```

>  **Do not commit your API key to version control.** Consider moving it to a `.env` file or environment variable.

---

## Usage

### Run directly

```bash
python3 identify_once.py
```

### Run via voice command (macOS)

The script is wrapped in an **Automator Application** so it runs with full macOS permissions (camera, audio) and the correct Homebrew Python environment.

In the **Shortcuts** app, an *Open App* action points to the Automator `.app`, named `"Identify Plant"`.

Say: **"Hey Siri, run Identify Plant"**

This approach avoids the shell sandbox limitations of running scripts directly from Shortcuts, and ensures the app properly prompts for camera and microphone access.

---

## Code Overview

**`identify_once.py`**

| Function | Description |
|---|---|
| `capture_image(device_name)` | Captures a single frame from the specified camera using `imagesnap` |
| `identify_image(path)` | Encodes the image and queries the Plant.id API; returns the top common name and confidence |
| `main()` | Orchestrates capture → identify → speak; announces the result via TTS |

---

## Example Output

> *"With 94.3% certainty, this is a Begonia rex."*

Tested identifications:
- *Anemone drummondii* (Blue windflower)
- *Begonia rex* (King begonia)
- *Cryptanthus bivittatus* (Earth star)

---

## Future Applications

Plant ID is just the beginning. This same glasses + API framework could support:

-  **Skin condition self-diagnosis** — reliable visual screening without Googling symptoms
-  **Name recall** — facial recognition to help people with memory conditions
-  **Assistive vision** — help the partially blind "see" and understand their surroundings
-  **General AI assistant** — never be confused about something you see again

---

## Acknowledgements

- **Mr. Nassar** — for ordering materials and keeping the project grounded in what was achievable
- **WT** — for funding the materials
- **Mr. Asanikar** — for lending smart glasses for early prototyping
- **[Plant.id API](https://plant.id/)** — the plant identification service powering the core feature

---

## License

MIT License — see `LICENSE` for details.
