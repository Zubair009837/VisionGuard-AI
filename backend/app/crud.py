from sqlalchemy.orm import Session

from .models import Camera
from .schemas import CameraCreate

from .config import NVRS

from .device_info import fetch_device_info
from .device_registry import register_device
from .identity_checker import check_identity
from .alert_manager import process_camera

from .ip_conflict_checker import (
    check_ip_conflicts,
    print_conflicts,
)

import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth


# ==========================================================
# XML Downloader
# ==========================================================

def fetch_xml(url, username, password):

    try:

        response = requests.get(
            url,
            auth=HTTPDigestAuth(
                username,
                password
            ),
            timeout=10
        )

        response.raise_for_status()

        return ET.fromstring(response.text)

    except Exception as e:

        print("Fetch Error :", e)

        return None


# ==========================================================
# Parse Camera List
# ==========================================================

def parse_channels(root):

    cameras = {}

    if root is None:
        return cameras

    for channel in root.findall(".//{*}InputProxyChannel"):

        id_node = channel.find("{*}id")

        if id_node is None:
            continue

        camera_id = int(id_node.text)

        name = f"Camera {camera_id}"

        name_node = channel.find("{*}name")

        if (
            name_node is not None
            and name_node.text
        ):
            name = name_node.text.strip()

        ip = ""

        source = channel.find(
            "{*}sourceInputPortDescriptor"
        )

        if source is not None:

            ip_node = source.find("{*}ipAddress")

            if (
                ip_node is not None
                and ip_node.text
            ):
                ip = ip_node.text.strip()

        cameras[camera_id] = {
            "name": name,
            "ip": ip
        }

    return cameras


# ==========================================================
# Parse Camera Status
# ==========================================================

def parse_status(root):

    status = {}

    if root is None:
        return status

    for channel in root.findall(
        ".//{*}InputProxyChannelStatus"
    ):

        id_node = channel.find("{*}id")

        if id_node is None:
            continue

        camera_id = int(id_node.text)

        online = channel.find("{*}online")

        status[camera_id] = (
            "Online"
            if (
                online is not None
                and online.text
                and online.text.lower() == "true"
            )
            else "Offline"
        )

    return status
# ==========================================================
# Scan All NVRs
# ==========================================================

def get_cameras(db: Session):

    all_cameras = []

    print("\n" + "=" * 70)
    print("VisionGuard AI Camera Scan Started")
    print("=" * 70)

    for nvr in NVRS:

        print(f"\n🔍 Scanning {nvr['name']} ...")

        channels_url = (
            f"http://{nvr['ip']}:{nvr['port']}"
            "/ISAPI/ContentMgmt/InputProxy/channels"
        )

        status_url = (
            f"http://{nvr['ip']}:{nvr['port']}"
            "/ISAPI/ContentMgmt/InputProxy/channels/status"
        )

        try:

            channels_root = fetch_xml(
                channels_url,
                nvr["username"],
                nvr["password"]
            )

            status_root = fetch_xml(
                status_url,
                nvr["username"],
                nvr["password"]
            )

            channels = parse_channels(channels_root)
            status = parse_status(status_root)

            device_info = fetch_device_info(
                nvr["ip"],
                nvr["port"],
                nvr["username"],
                nvr["password"],
            )

            if device_info is None:
                device_info = {}

            print(f"📷 Cameras Found : {len(channels)}")

            for camera_id in sorted(channels.keys()):

                camera = {
                    "id": camera_id,
                    "name": channels[camera_id]["name"],
                    "ip": channels[camera_id]["ip"],
                    "status": status.get(camera_id, "Offline"),
                    "nvr": nvr["name"],
                    "serial": device_info.get("serial", ""),
                    "model": device_info.get("model", ""),
                    "firmware": device_info.get("firmware", ""),
                    "mac": device_info.get("mac", ""),
                }

                register_device(camera)
                check_identity(camera)
                process_camera(camera)

                all_cameras.append(camera)

                print(
                    f"   [{camera['status']}] "
                    f"{camera['name']} "
                    f"({camera['ip']})"
                )

        except Exception as e:

            print(f"❌ {nvr['name']} Error : {e}")
            continue

    print("\n" + "=" * 70)
    print(f"✅ Total Cameras : {len(all_cameras)}")
    print("=" * 70)

    if all_cameras:

        conflicts = check_ip_conflicts(all_cameras)
        print_conflicts(conflicts)

        return all_cameras

    print("⚠️ No Live Cameras Found. Loading Database...")

    return db.query(Camera).all()
# ==========================================================
# Create Camera
# ==========================================================

def create_camera(
    db: Session,
    camera: CameraCreate
):

    db_camera = Camera(
        name=camera.name,
        status=camera.status,
        nvr=camera.nvr,
        ip=camera.ip,
    )

    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)

    return db_camera


# ==========================================================
# Module Information
# ==========================================================

__version__ = "2.0 Enterprise"

print("\n" + "=" * 70)
print("✅ VisionGuard AI CRUD Engine Loaded")
print("=" * 70)