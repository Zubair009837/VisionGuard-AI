from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Camera
from .schemas import CameraCreate, CameraResponse
from . import crud

import os
import requests
from requests.auth import HTTPDigestAuth
from dotenv import load_dotenv

load_dotenv()

NVR_IP = os.getenv("NVR_IP")
NVR_PORT = os.getenv("NVR_PORT")
NVR_USERNAME = os.getenv("NVR_USERNAME")
NVR_PASSWORD = os.getenv("NVR_PASSWORD")

app = FastAPI(title="VisionGuard AI")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "VisionGuard AI Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    cameras = crud.get_cameras(db)

    total = len(cameras)
    online = len([c for c in cameras if c["status"] == "Online"])
    offline = total - online

    return {
        "total": total,
        "online": online,
        "offline": offline,
        "nvr": 1
    }


@app.get("/cameras", response_model=list[CameraResponse])
def get_cameras(db: Session = Depends(get_db)):
    return crud.get_cameras(db)


@app.post("/cameras", response_model=CameraResponse)
def create_camera(camera: CameraCreate, db: Session = Depends(get_db)):
    return crud.create_camera(db, camera)


@app.get("/nvr/status")
def nvr_status():

    if not NVR_IP or not NVR_PORT:
        return {
            "status": "CONFIGURATION_ERROR",
            "message": ".env file not configured correctly"
        }

    url = f"http://{NVR_IP}:{NVR_PORT}"

    try:
        response = requests.get(
    url,
    auth=HTTPDigestAuth(NVR_USERNAME, NVR_PASSWORD),
    timeout=5
)

        if response.status_code in [200, 401]:
            return {
                "status": "ONLINE",
                "ip": NVR_IP,
                "port": NVR_PORT
            }

        return {
            "status": "OFFLINE",
            "http_status": response.status_code
        }

    except Exception as e:
        return {
            "status": "OFFLINE",
            "error": str(e)
        }


@app.get("/nvr/raw", response_class=PlainTextResponse)
def nvr_raw():

    if not NVR_IP or not NVR_PORT:
        return "NVR Configuration Missing"

    url = f"http://{NVR_IP}:{NVR_PORT}/ISAPI/ContentMgmt/InputProxy/channels"

    try:
        response = requests.get(
    url,
    auth=HTTPDigestAuth(NVR_USERNAME, NVR_PASSWORD),
    timeout=10
)

        return response.text

    except Exception as e:
        return str(e)