import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import EMAIL_BRAND

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Sender
SENDER_EMAIL = "Zubair.khan@1mg.com"

# Gmail App Password
APP_PASSWORD = "garajkqynquqccpe"

# Receiver
RECEIVER_EMAIL = "Zubair.khan@1mg.com"


# HTML Templates Folder
TEMPLATE_DIR = Path(__file__).parent / "templates"


def render_template(template_name: str, data: dict):

    template_path = TEMPLATE_DIR / template_name

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    for key, value in data.items():
        html = html.replace("{{" + key + "}}", str(value))

    return html


def send_html_email(
    *,
    subject: str,
    template_name: str,
    camera: str,
    nvr: str,
    ip: str,
    status: str,
    event_time: str,
):
    """
    Generic HTML Email Sender
    """

    try:

        html = render_template(
    template_name,
    {
        "brand": EMAIL_BRAND,
        "camera": camera,
        "nvr": nvr,
        "ip": ip,
        "status": status,
        "issues": status,
        "time": event_time,
    },
)

        msg = MIMEMultipart("alternative")

        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject

        msg.attach(MIMEText(html, "html"))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        server.ehlo()

        server.starttls()

        server.ehlo()

        server.login(SENDER_EMAIL, APP_PASSWORD)

        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAIL,
            msg.as_string()
        )

        server.quit()

        print(f"✅ Email Sent : {camera}")

        return True

    except Exception as e:

        print("❌ Email Error :", e)

        return False


# =====================================================
# CAMERA OFFLINE EMAIL
# =====================================================

def send_offline_email(
    camera,
    nvr,
    ip,
    event_time
):

    return send_html_email(

        subject=f"🔴 [{nvr}] Camera Offline - {camera}",

        template_name="offline.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        status="OFFLINE",

        event_time=event_time

    )


# =====================================================
# CAMERA RECOVERY EMAIL
# =====================================================

def send_recovery_email(
    camera,
    nvr,
    ip,
    event_time
):

    return send_html_email(

        subject=f"🟢 [{nvr}] Camera Recovered - {camera}",

        template_name="recovery.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        status="ONLINE",

        event_time=event_time

    )

# =====================================================
# DEVICE IDENTITY EMAIL
# =====================================================

def send_identity_email(
    camera,
    nvr,
    ip,
    issues,
    event_time
):

    return send_html_email(

        subject=f"🚨 [{nvr}] Device Identity Changed - {camera}",

        template_name="identity.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        status=issues,

        event_time=event_time

    )


# =====================================================
# IP CONFLICT EMAIL
# =====================================================

def send_ip_conflict_email(
    camera,
    nvr,
    ip,
    event_time
):

    return send_html_email(

        subject=f"⚠️ [{nvr}] IP Conflict - {camera}",

        template_name="ip_conflict.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        status="Duplicate IP Detected",

        event_time=event_time

    )

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    send_offline_email(

        camera="SRN INBOUND",

        nvr="NVR-2",

        ip="192.168.1.116",

        event_time="03 Aug 2026 05:10 PM"

    )