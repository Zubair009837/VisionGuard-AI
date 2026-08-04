import threading
import time
from datetime import datetime
import cv2
import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth

from .config import NVRS
from .email_service import (
    send_video_loss_email,
    send_video_restored_email,
)

# ==========================================================
# VisionGuard AI Enterprise Video Monitor
# ==========================================================

CHECK_INTERVAL = 10
REQUEST_TIMEOUT = 8

# Camera status memory
CAMERA_STATUS = {}

# Prevent duplicate alerts
LOSS_ALERT_SENT = set()
RESTORE_ALERT_SENT = set()

print("=" * 70)
print("VisionGuard AI Enterprise Video Monitor Loaded")
print("=" * 70)


# ==========================================================
# Fetch Streaming Channels
# ==========================================================

def get_stream_channels(nvr):

    url = (
        f"http://{nvr['ip']}:{nvr['port']}"
        "/ISAPI/Streaming/channels"
    )

    try:

        response = requests.get(
            url,
            auth=HTTPDigestAuth(
                nvr["username"],
                nvr["password"]
            ),
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        root = ET.fromstring(response.text)

        channels = []

        for channel in root.findall(".//{*}StreamingChannel"):

            id_node = channel.find("{*}id")

            if id_node is None:
                continue

            stream_id = id_node.text.strip()

            input_node = channel.find("{*}dynVideoInputChannelID")

            camera_no = (
                input_node.text.strip()
                if input_node is not None
                else stream_id
            )

            channels.append({
                "stream_id": stream_id,
                "camera": f"Camera {camera_no}"
            })

        return channels

    except Exception as e:

        print(f"[{nvr['name']}] Channel Fetch Error : {e}")

        return []
# ==========================================================
# Check RTSP Stream
# ==========================================================

import cv2

def stream_alive(nvr, stream_id):

    rtsp_url = (
        f"rtsp://"
        f"{nvr['username']}:"
        f"{nvr['password']}@"
        f"{nvr['ip']}:554/"
        f"Streaming/Channels/{stream_id}"
    )

    cap = None

    try:

        cap = cv2.VideoCapture(
            rtsp_url,
            cv2.CAP_FFMPEG
        )

        if not cap.isOpened():
            return False

        ok, frame = cap.read()

        return ok and frame is not None

    except Exception:

        return False

    finally:

        if cap is not None:
            cap.release()


# ==========================================================
# Check Single Camera
# ==========================================================

def check_camera(nvr, channel):

    stream_id = channel["stream_id"]

    camera_name = channel["camera"]

    key = f"{nvr['name']}-{camera_name}"

    current_status = stream_alive(
        nvr,
        stream_id
    )

    previous_status = CAMERA_STATUS.get(key)

    # First Scan
    if previous_status is None:

        CAMERA_STATUS[key] = current_status

        return

    # ------------------------------------------------------
    # Video Loss
    # ------------------------------------------------------

    if previous_status and not current_status:

        if key not in LOSS_ALERT_SENT:

            print(f"❌ VIDEO LOST : {key}")

            send_video_loss_email(

                camera=camera_name,

                nvr=nvr["name"],

                ip=nvr["ip"],

                event_time=datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            LOSS_ALERT_SENT.add(key)

            RESTORE_ALERT_SENT.discard(key)

    # ------------------------------------------------------
    # Video Restored
    # ------------------------------------------------------

    elif (not previous_status) and current_status:

        if key not in RESTORE_ALERT_SENT:

            print(f"✅ VIDEO RESTORED : {key}")

            send_video_restored_email(

                camera=camera_name,

                nvr=nvr["name"],

                ip=nvr["ip"],

                event_time=datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            RESTORE_ALERT_SENT.add(key)

            LOSS_ALERT_SENT.discard(key)

    CAMERA_STATUS[key] = current_status
# ==========================================================
# Check Complete NVR
# ==========================================================

def check_nvr(nvr):

    print(f"\nChecking {nvr['name']}...")

    channels = get_stream_channels(nvr)

    if not channels:

        print(f"{nvr['name']} : No Streaming Channels Found")

        return

    print(f"Found {len(channels)} Cameras")

    online = 0
    offline = 0

    for channel in channels:

        try:

            alive = stream_alive(
                nvr,
                channel["stream_id"]
            )

            if alive:
                online += 1
            else:
                offline += 1

            check_camera(
                nvr,
                channel
            )

        except Exception as e:

            print(
                f"{channel['camera']} Error : {e}"
            )

    print(
        f"{nvr['name']} Summary : "
        f"{online} Online | "
        f"{offline} Offline"
    )
# ==========================================================
# Monitor All NVRs
# ==========================================================

def monitor_all_nvrs():

    print("=" * 70)
    print("VIDEO MONITOR STARTED")
    print("=" * 70)

    while True:

        start_time = time.time()

        for nvr in NVRS:

            try:

                check_nvr(nvr)

            except Exception as e:

                print(
                    f"{nvr['name']} Error : {e}"
                )

        elapsed = time.time() - start_time

        if elapsed < CHECK_INTERVAL:

            time.sleep(
                CHECK_INTERVAL - elapsed
            )


# ==========================================================
# Background Thread
# ==========================================================

def start_video_monitor():

    monitor_thread = threading.Thread(

        target=monitor_all_nvrs,

        daemon=True,

        name="VisionGuardVideoMonitor"

    )

    monitor_thread.start()

    print("=" * 70)
    print("Background Monitor Thread Started")
    print("=" * 70)
# ==========================================================
# Manual Check
# ==========================================================

def run_once():

    print("=" * 70)
    print("Running One-Time Video Health Check")
    print("=" * 70)

    for nvr in NVRS:

        try:

            check_nvr(nvr)

        except Exception as e:

            print(f"{nvr['name']} Error : {e}")


# ==========================================================
# Main Entry
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("VisionGuard AI Enterprise Video Monitor")
    print("=" * 70)

    start_video_monitor()

    try:

        while True:

            time.sleep(60)

    except KeyboardInterrupt:

        print("\nStopping Video Monitor...")

        print("Video Monitor Stopped Successfully.")
# ==========================================================
# Check Single Camera
# ==========================================================

def check_camera(nvr, channel):

    global TOTAL_VIDEO_LOSS
    global TOTAL_VIDEO_RESTORED

    stream_id = channel["stream_id"]
    camera_name = channel["camera"]

    key = f"{nvr['name']}-{camera_name}"

    current_status = stream_alive(
        nvr,
        stream_id
    )

    previous_status = CAMERA_STATUS.get(key)

    # First Scan
    if previous_status is None:

        CAMERA_STATUS[key] = current_status
        return

    # ------------------------------------------------------
    # Video Lost
    # ------------------------------------------------------

    if previous_status and not current_status:

        if key not in LOSS_ALERT_SENT:

            print(f"❌ VIDEO LOST : {key}")

            VIDEO_LOSS_TIME[key] = datetime.now()

            TOTAL_VIDEO_LOSS += 1

            send_video_loss_email(
                camera=camera_name,
                nvr=nvr["name"],
                ip=nvr["ip"],
                event_time=datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            LOSS_ALERT_SENT.add(key)
            RESTORE_ALERT_SENT.discard(key)

    # ------------------------------------------------------
    # Video Restored
    # ------------------------------------------------------

    elif (not previous_status) and current_status:

        if key not in RESTORE_ALERT_SENT:

            print(f"✅ VIDEO RESTORED : {key}")

            TOTAL_VIDEO_RESTORED += 1

            start = VIDEO_LOSS_TIME.pop(key, None)

            if start:

                duration = datetime.now() - start

                print(
                    f"{key} Downtime : {duration}"
                )

            send_video_restored_email(
                camera=camera_name,
                nvr=nvr["name"],
                ip=nvr["ip"],
                event_time=datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            RESTORE_ALERT_SENT.add(key)
            LOSS_ALERT_SENT.discard(key)

    CAMERA_STATUS[key] = current_status
# ==========================================================
# Enterprise Event Logger
# ==========================================================

import json
import os

BASE_DIR = os.path.dirname(__file__)

EVENT_LOG_FILE = os.path.join(
    BASE_DIR,
    "video_monitor_history.json"
)


def load_event_history():

    if not os.path.exists(EVENT_LOG_FILE):
        return []

    try:

        with open(
            EVENT_LOG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return []


EVENT_HISTORY = load_event_history()


def save_event_history():

    try:

        with open(
            EVENT_LOG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                EVENT_HISTORY,
                f,
                indent=4
            )

    except Exception as e:

        print("History Save Error :", e)


def log_video_event(
    event,
    nvr,
    camera,
    ip,
    downtime=None
):

    EVENT_HISTORY.append({

        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "event": event,

        "nvr": nvr,

        "camera": camera,

        "ip": ip,

        "downtime": downtime

    })

    if len(EVENT_HISTORY) > 5000:

        EVENT_HISTORY.pop(0)

    save_event_history()


# ==========================================================
# History Viewer
# ==========================================================

def print_recent_events(limit=20):

    print("\n" + "=" * 70)
    print("Recent Video Events")
    print("=" * 70)

    for event in EVENT_HISTORY[-limit:]:

        print(
            f"{event['time']} | "
            f"{event['event']} | "
            f"{event['nvr']} | "
            f"{event['camera']}"
        )

    print("=" * 70)


# ==========================================================
# Enterprise Health Report
# ==========================================================

def print_health_report():

    print("\n" + "=" * 70)

    print("VisionGuard AI Health Report")

    print("=" * 70)

    print(f"Total Cameras          : {len(CAMERA_STATUS)}")
    print(f"Current Video Loss     : {len(LOSS_ALERT_SENT)}")
    print(f"Video Loss Events      : {TOTAL_VIDEO_LOSS}")
    print(f"Video Restore Events   : {TOTAL_VIDEO_RESTORED}")
    print(f"History Records        : {len(EVENT_HISTORY)}")

    print("=" * 70)
# ==========================================================
# Graceful Shutdown
# ==========================================================

def stop_video_monitor():

    print("\n" + "=" * 70)
    print("Stopping VisionGuard AI Video Monitor...")
    print("=" * 70)

    try:

        print_health_report()

        print_recent_events(10)

    except Exception as e:

        print("Shutdown Report Error :", e)

    print("Video Monitor Stopped Successfully.")


# ==========================================================
# Enterprise Startup
# ==========================================================

def start_enterprise_monitor():

    print("=" * 70)
    print("VisionGuard AI Enterprise Video Monitoring Engine")
    print("=" * 70)

    print(f"Loaded NVRs : {len(NVRS)}")
    print(f"Check Interval : {CHECK_INTERVAL} Seconds")
    print("Alert Engine : Enabled")
    print("History Logger : Enabled")
    print("Duplicate Protection : Enabled")
    print("=" * 70)

    start_video_monitor()


# ==========================================================
# Manual Test
# ==========================================================

if __name__ == "__main__":

    try:

        start_enterprise_monitor()

        while True:

            time.sleep(60)

    except KeyboardInterrupt:

        stop_video_monitor()