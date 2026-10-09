"""
Rajasthan Tourism AI Avatar Generator (D-ID) — Talkative & Lively Mode
========================================================================
Uses D-ID's Lively Motion Driver (bank://lively/driver-06) and Fluent animation
to make the avatar animated, expressive, and talkative with rich head tilts,
facial expressions, and conversational storytelling!

Usage:
    python create_did_video.py
"""

import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import webbrowser

# Ensure Windows console supports UTF-8 safely without UnicodeEncodeError
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# D-ID API Credentials
API_KEY = "Z29vZ2xlLW9hdXRoMnwxMDU2NDU3ODA5ODM0MzY0MzAyNzdAYWtfVzh5Nl9MQzdwTEg3ZTA4dDlteVRz:AYPI15kyrZV76D_WmDhuB"
AUTH_HEADER = "Basic " + base64.b64encode(API_KEY.encode()).decode()

OUTPUT_FILE = "rajasthan_tourism_talkative.mp4"

# Lively, conversational, and talkative script
TALKATIVE_SCRIPT = (
    "Arey Khamma Ghani, my friend! Come on in, let me share a royal secret with you. "
    "When you visit Rajasthan, you do not just see history - you live it! "
    "Have you ever climbed the winding ramparts of Mehrangarh as the desert wind sings ancient warrior songs? "
    "Or tasted piping hot Dal Baati Churma with sweet ghevar in a buzzing night bazaar? "
    "From regal courtyards to starlit sand dunes, every moment is pure magic. "
    "Tell me, when are you visiting? Padharo Mhare Des!"
)

def log(msg):
    try:
        print(msg, flush=True)
    except Exception:
        try:
            print(msg.encode('ascii', 'replace').decode('ascii'), flush=True)
        except Exception:
            pass

def open_file_locally(filepath):
    """Opens video with Windows default media player."""
    try:
        if os.name == 'nt':
            os.startfile(filepath)
        else:
            webbrowser.open("file://" + os.path.abspath(filepath))
        log(f"Playing video in media player: {filepath}")
    except Exception as e:
        log(f"Could not auto-launch player ({e}). You can open '{filepath}' manually.")

def check_credits():
    """Checks remaining credits on D-ID account."""
    req = urllib.request.Request(
        "https://api.d-id.com/credits",
        headers={"Authorization": AUTH_HEADER, "Accept": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        remaining = data.get("remaining", "N/A")
        log(f"[OK] D-ID Account Connected! Remaining Credits: {remaining}")
        return remaining

def download_video(video_url, destination=OUTPUT_FILE):
    """Downloads the MP4 from D-ID cloud to local disk."""
    log(f"Downloading high-definition talkative video from D-ID...")
    urllib.request.urlretrieve(video_url, destination)
    log(f"[OK] Video saved successfully to: {os.path.abspath(destination)}")
    return os.path.abspath(destination)

def main():
    log("========================================================")
    log("   Rajasthan Tourism Avatar — Talkative & Lively Mode")
    log("========================================================\n")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_video = os.path.join(current_dir, OUTPUT_FILE)

    # 1. If this lively video already exists, launch it!
    if os.path.exists(local_video) and os.path.getsize(local_video) > 100000:
        log(f"[SUCCESS] Talkative video already downloaded on your computer!")
        log(f"File: {local_video} ({round(os.path.getsize(local_video)/(1024*1024), 2)} MB)\n")
        open_file_locally(local_video)
        return

    check_credits()

    log("\nInitiating D-ID render with Lively Driver (dynamic facial expressions & head motion)...")
    image_url = "s3://d-id-images-prod/google-oauth2|105645780983436430277/img_2DT4ccj-uSfTN5PhaGZ3a/avatar.jpg"

    payload = {
        "source_url": image_url,
        "driver_url": "bank://lively/driver-06",
        "script": {
            "type": "text",
            "subtitles": False,
            "provider": {
                "type": "microsoft",
                "voice_id": "en-IN-NeerjaNeural"
            },
            "input": TALKATIVE_SCRIPT
        },
        "config": {
            "fluent": True,
            "pad_audio": 0.0
        }
    }

    req = urllib.request.Request(
        "https://api.d-id.com/talks",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": AUTH_HEADER,
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(req) as resp:
        talk_data = json.loads(resp.read().decode())
        talk_id = talk_data.get("id")
        log(f"Job submitted to D-ID! Job ID: {talk_id}")

    # Poll D-ID until completion
    log("Rendering lively lip-sync and dynamic expressions (this takes ~30-60s)...")
    for attempt in range(80):
        time.sleep(3)
        poll_req = urllib.request.Request(
            f"https://api.d-id.com/talks/{talk_id}",
            headers={"Authorization": AUTH_HEADER, "Accept": "application/json"}
        )
        with urllib.request.urlopen(poll_req) as resp:
            data = json.loads(resp.read().decode())
            status = data.get("status")
            log(f"Progress ({attempt+1}): {status}...")
            if status == "done":
                result_url = data.get("result_url")
                saved_path = download_video(result_url, local_video)
                open_file_locally(saved_path)
                return
            elif status == "error":
                log(f"[ERROR] D-ID rendering failed: {data}")
                return

    log("Rendering took too long. Check https://studio.d-id.com")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"\n[ERROR]: {e}")
