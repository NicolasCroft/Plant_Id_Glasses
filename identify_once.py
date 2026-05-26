#!/opt/homebrew/bin/python3.11

import subprocess, tempfile, io, base64, json, requests, pyttsx3, os
from PIL import Image

# --- Config ---
IMGSNAP = "/opt/homebrew/bin/imagesnap"
API_KEY = os.environ.get("PLANT_ID_API_KEY", "your_api_key_here")
API_URL = "https://api.plant.id/v2/identify"

# TTS setup
tts = pyttsx3.init()
for v in tts.getProperty('voices'):
    if 'female' in v.name.lower() or 'samantha' in v.id.lower():
        tts.setProperty('voice', v.id)
        break
tts.setProperty('rate', 120)

def capture_image(device_name: str = None):
    """
    Grab one frame from the specified camera (or default) into a temp file.
    If device_name is given, pass it via -d to imagesnap.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    path = tmp.name
    tmp.close()

    cmd = [IMGSNAP]
    if device_name:
        cmd += ["-d", device_name]
    cmd += ["-w", "0.5", path]

    subprocess.run(cmd, check=True)
    return path

def identify_image(path):
    with Image.open(path) as img:
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        img_bytes = buf.getvalue()

    img_b64 = base64.b64encode(img_bytes).decode()
    payload = {
        "images": [img_b64],
        "modifiers": ["crops_fast", "similar_images"],
        "plant_language": "en",
        "plant_details": ["common_names"]
    }
    headers = {"Content-Type": "application/json", "Api-Key": API_KEY}

    resp = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=20)
    resp.raise_for_status()
    sugg = resp.json().get("suggestions", [])
    if not sugg:
        return None, 0.0

    top = sugg[0]
    prob = top.get("probability", 0.0)
    details = top.get("plant_details", {})
    common = details.get("common_names", [])
    display = common[0] if common else top.get("plant_name", "Unknown")
    return display, prob

def main():
    img_path = capture_image("HD Camera")
    name, prob = identify_image(img_path)
    os.remove(img_path)

    if not name:
        phrase = "Sorry, I couldn’t find a match."
    else:
        pct = round(prob * 100, 1)
        phrase = f"With {pct}% certainty, this is a {name}."

    tts.say(phrase)
    tts.runAndWait()

if __name__ == "__main__":
    main()
