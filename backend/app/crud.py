from .identity_checker import check_identity
from .ip_conflict_checker import check_ip_conflicts, print_conflicts
from .device_info import fetch_device_info
from sqlalchemy.orm import Session
from .models import Camera
from .schemas import CameraCreate
from .config import NVRS
from .alert_manager import process_camera
from .device_registry import register_device
from .identity_checker import check_identity
from .ip_conflict_checker import (
    check_ip_conflicts,
    print_conflicts,
)

import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth


def fetch_xml(url, username, password):
    try:
        response = requests.get(
            url,
            auth=HTTPDigestAuth(username, password),
            timeout=10,
        )
        response.raise_for_status()
        return ET.fromstring(response.text)
    except Exception as e:
        print("Fetch Error :", e)
        return None


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
        if name_node is not None and name_node.text:
            name = name_node.text.strip()

        ip = ""
        source = channel.find("{*}sourceInputPortDescriptor")
        if source is not None:
            ip_node = source.find("{*}ipAddress")
            if ip_node is not None and ip_node.text:
                ip = ip_node.text.strip()

        cameras[camera_id] = {"name": name, "ip": ip}

    return cameras


def parse_status(root):
    status = {}

    if root is None:
        return status

    for channel in root.findall(".//{*}InputProxyChannelStatus"):
        id_node = channel.find("{*}id")
        if id_node is None:
            continue

        camera_id = int(id_node.text)
        online = channel.find("{*}online")

        status[camera_id] = (
            "Online"
            if online is not None and online.text and online.text.lower() == "true"
            else "Offline"
        )

    return status


def get_cameras(db: Session):
    all_cameras = []

    for nvr in NVRS:
        print(f"Scanning {nvr['name']} ...")

        channels_url = (
            f"http://{nvr['ip']}:{nvr['port']}/ISAPI/ContentMgmt/InputProxy/channels"
        )
        status_url = (
            f"http://{nvr['ip']}:{nvr['port']}/ISAPI/ContentMgmt/InputProxy/channels/status"
        )

        try:
            channels_root = fetch_xml(
                channels_url, nvr["username"], nvr["password"]
            )
            status_root = fetch_xml(
                status_url, nvr["username"], nvr["password"]
            )

            channels = parse_channels(channels_root)
            status = parse_status(status_root)

            device_info = fetch_device_info(
                nvr["ip"],
                nvr["port"],
                nvr["username"],
                nvr["password"],
            )

            print(f"{nvr['name']} Cameras :", len(channels))

            for camera_id in channels:
                camera = {
                    "id": camera_id,
                    "name": channels[camera_id]["name"],
                    "ip": channels[camera_id]["ip"],
                    "status": status.get(camera_id, "Offline"),
                    "nvr": nvr["name"],
                    "serial": device_info["serial"],
                    "model": device_info["model"],
                    "firmware": device_info["firmware"],
                    "mac": device_info["mac"],
                }

                register_device(camera)
                check_identity(camera)
                process_camera(camera)
                all_cameras.append(camera)

        except Exception as e:
            print(f"{nvr['name']} Error : {e}")
            continue

    if all_cameras:
        print("----------------------------------")
        print("Total Cameras :", len(all_cameras))
        print("----------------------------------")

        conflicts = check_ip_conflicts(all_cameras)
        print_conflicts(conflicts)

        return all_cameras

    return db.query(Camera).all()


def create_camera(db: Session, camera: CameraCreate):
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
