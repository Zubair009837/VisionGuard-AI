from sqlalchemy.orm import Session
from .models import Camera
from .schemas import CameraCreate

import os
import requests
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
from requests.auth import HTTPDigestAuth

load_dotenv()

NVR_IP = os.getenv("NVR_IP")
NVR_PORT = os.getenv("NVR_PORT")
NVR_USERNAME = os.getenv("NVR_USERNAME")
NVR_PASSWORD = os.getenv("NVR_PASSWORD")


def get_cameras(db: Session):

    url = f"http://{NVR_IP}:{NVR_PORT}/ISAPI/ContentMgmt/InputProxy/channels"

    try:
        response = requests.get(
            url,
            auth=HTTPDigestAuth(NVR_USERNAME, NVR_PASSWORD),
            timeout=10,
        )

        response.raise_for_status()

        root = ET.fromstring(response.text)

        cameras = []

        for channel in root.findall(".//{*}InputProxyChannel"):

            camera = {
                "id": 0,
                "name": "",
                "ip": "",
                "status": "Online",
                "nvr": "Hikvision",
            }

            id_node = channel.find("{*}id")
            if id_node is not None and id_node.text:
                camera["id"] = int(id_node.text)

            name_node = channel.find("{*}name")
            if name_node is not None and name_node.text:
                camera["name"] = name_node.text.strip()

            source = channel.find("{*}sourceInputPortDescriptor")
            if source is not None:
                ip_node = source.find("{*}ipAddress")
                if ip_node is not None and ip_node.text:
                    camera["ip"] = ip_node.text.strip()

            cameras.append(camera)

        return cameras

    except Exception as e:
        print("NVR Error:", e)
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