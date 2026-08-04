from datetime import datetime
import time
import requests
import xml.etree.ElementTree as ET

from requests.auth import HTTPDigestAuth

from .config import NVRS
from .email_service import (
    send_offline_email,
    send_recovery_email,
)

# ==========================================================
# VisionGuard AI Camera Monitor
# ==========================================================

class CameraMonitor:

    def __init__(self):

        # Current status
        self.camera_status = {}

        # Last email status
        self.email_sent = {}

        # Recovery tracking
        self.recovery_sent = {}

        # Last check time
        self.last_seen = {}

    def get_nvr_channels(self, nvr):

        """
        Read camera channels from Hikvision ISAPI
        """

        url = (
            f"http://{nvr['ip']}:{nvr['port']}"
            "/ISAPI/ContentMgmt/InputProxy/channels/status"
        )

        try:

            response = requests.get(
                url,
                auth=HTTPDigestAuth(
                    nvr["username"],
                    nvr["password"]
                ),
                timeout=10
            )

            if response.status_code == 200:
                return response.text

        except Exception as e:

            print(f"[{nvr['name']}] {e}")

        return None

# ==========================================================
# XML Parser
# ==========================================================

    def parse_channels(self, xml_data):

        """
        Parse Hikvision channel status XML.
        """

        cameras = []

        if not xml_data:
            return cameras

        try:

            root = ET.fromstring(xml_data)

            for channel in root.iter():

                if "InputProxyChannelStatus" in channel.tag:

                    camera = {

                        "id": "",
                        "name": "",
                        "ip": "",
                        "status": "Offline"

                    }

                    for child in channel:

                        tag = child.tag.split("}")[-1]

                        if tag == "id":
                            camera["id"] = child.text

                        elif tag == "name":
                            camera["name"] = child.text

                        elif tag == "ipAddress":
                            camera["ip"] = child.text

                        elif tag == "online":
                            camera["status"] = (
                                "Online"
                                if child.text == "true"
                                else "Offline"
                            )

                    cameras.append(camera)

        except Exception as e:

            print("XML Parse Error :", e)

        return cameras


# ==========================================================
# Camera Scanner
# ==========================================================

    def scan_nvr(self, nvr):

        xml = self.get_nvr_channels(nvr)

        cameras = self.parse_channels(xml)

        return cameras
    # ==========================================================
# Offline / Recovery Detection
# ==========================================================

    def process_cameras(self, cameras, nvr_name):

        """
        Process all cameras from one NVR.
        """

        for camera in cameras:

            key = f"{nvr_name}_{camera['id']}"

            current_status = camera["status"]

            previous_status = self.camera_status.get(
                key,
                "Unknown"
            )

            # Save latest status
            self.camera_status[key] = current_status

            # Save last seen time
            self.last_seen[key] = datetime.now()

            # --------------------------------------
            # Camera Offline
            # --------------------------------------

            if (
                current_status == "Offline"
                and previous_status != "Offline"
            ):

                print(
                    f"[OFFLINE] {camera['name']} "
                    f"({camera['ip']})"
                )

                send_offline_email(

                    camera=camera["name"],

                    nvr=nvr_name,

                    ip=camera["ip"],

                    event_time=datetime.now().strftime(
                        "%d-%b-%Y %H:%M:%S"
                    )

                )

                self.email_sent[key] = True

                self.recovery_sent[key] = False

            # --------------------------------------
            # Camera Recovery
            # --------------------------------------

            elif (

                current_status == "Online"

                and previous_status == "Offline"

            ):

                print(
                    f"[RECOVERY] {camera['name']}"
                )

                send_recovery_email(

                    camera=camera["name"],

                    nvr=nvr_name,

                    ip=camera["ip"],

                    event_time=datetime.now().strftime(
                        "%d-%b-%Y %H:%M:%S"
                    )

                )

                self.email_sent[key] = False

                self.recovery_sent[key] = True
                # ==========================================================
# Monitor All NVRs
# ==========================================================

    def scan_all_nvrs(self):

        """
        Scan every configured NVR once.
        """

        for nvr in NVRS:

            try:

                cameras = self.scan_nvr(nvr)

                if cameras:

                    self.process_cameras(
                        cameras,
                        nvr["name"]
                    )

            except Exception as e:

                print(
                    f"[{nvr['name']}] Monitor Error : {e}"
                )


# ==========================================================
# Continuous Monitoring Loop
# ==========================================================

    def start(self):

        """
        Start VisionGuard AI Monitoring Engine.
        """

        print("=" * 60)
        print("VISIONGUARD AI ENTERPRISE")
        print("Camera Monitoring Engine Started")
        print("=" * 60)

        while True:

            try:

                self.scan_all_nvrs()

            except Exception as e:

                print("Monitoring Error :", e)

            time.sleep(5)


# ==========================================================
# Singleton Monitor Instance
# ==========================================================

monitor = CameraMonitor()
