from datetime import datetime
import time
import json
from pathlib import Path

from .config import (
    ALERT_DELAY_SECONDS,
    ENABLE_DUPLICATE_PROTECTION
)

from .email_service import (
    send_offline_email,
    send_recovery_email
)

# =====================================
# Runtime Storage
# =====================================

camera_status = {}

offline_since = {}

alert_sent = {}

HISTORY_FILE = Path(__file__).parent / "alert_history.json"


def save_history(camera, status):

    history = []

    if HISTORY_FILE.exists():

        try:

            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)

        except:
            history = []

    history.append({

        "camera": camera["name"],

        "nvr": camera["nvr"],

        "ip": camera["ip"],

        "status": status,

        "time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:

        json.dump(history, f, indent=4)
def process_camera(camera):

    key = f"{camera['nvr']}_{camera['id']}"

    current = camera["status"]

    if key not in camera_status:

        camera_status[key] = current

        if current == "Offline":
            offline_since[key] = time.time()

        return

    previous = camera_status[key]

    # ============================
    # Camera Offline
    # ============================

    if current == "Offline":

        if key not in offline_since:

            offline_since[key] = time.time()

        elapsed = time.time() - offline_since[key]

        if elapsed >= ALERT_DELAY_SECONDS:

            if ENABLE_DUPLICATE_PROTECTION:

                if alert_sent.get(key):

                    return

            send_offline_email(

                camera=camera["name"],

                nvr=camera["nvr"],

                ip=camera["ip"],

                event_time=datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

            )

            save_history(camera, "Offline")

            alert_sent[key] = True
    # ============================
    # Camera Recovered
    # ============================

    elif current == "Online":

        if previous == "Offline":

            send_recovery_email(

                camera=camera["name"],

                nvr=camera["nvr"],

                ip=camera["ip"],

                event_time=datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

            )

            save_history(camera, "Recovered")

        # Reset alert state
        if key in offline_since:
            del offline_since[key]

        if key in alert_sent:
            del alert_sent[key]

    # ============================
    # Update Current Status
    # ============================

    camera_status[key] = current
    # =====================================
# Generic Alert (Video Loss etc.)
# =====================================

def add_alert(
    alert_type,
    severity,
    title,
    description,
):

    history = []

    if HISTORY_FILE.exists():

        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)

        except:
            history = []

    history.append({

        "type": alert_type,

        "severity": severity,

        "title": title,

        "description": description,

        "time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:

        json.dump(history, f, indent=4)

    print(f"[{severity}] {title}")