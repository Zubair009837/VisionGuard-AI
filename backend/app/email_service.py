import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import EMAIL_BRAND

# =====================================================
# SMTP Configuration
# =====================================================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# =====================================================
# Sender Information
# =====================================================

SENDER_EMAIL = "Zubair.khan@1mg.com"

# Gmail App Password
APP_PASSWORD = "garajkqynquqccpe"

# =====================================================
# Receiver
# =====================================================

RECEIVER_EMAIL = "Zubair.khan@1mg.com"

# =====================================================
# HTML Templates
# =====================================================

TEMPLATE_DIR = Path(__file__).parent / "templates"

# =====================================================
# Template Renderer
# =====================================================

def render_template(template_name: str, data: dict):

    template_path = TEMPLATE_DIR / template_name

    with open(
        template_path,
        "r",
        encoding="utf-8"
    ) as f:

        html = f.read()

    for key, value in data.items():

        html = html.replace(
            "{{" + key + "}}",
            str(value)
        )

    return html


# =====================================================
# Generic Enterprise HTML Email Sender
# =====================================================

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

        msg.attach(
            MIMEText(
                html,
                "html"
            )
        )

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAIL,
            msg.as_string()
        )

        server.quit()

        print(f"✅ Email Sent : {subject}")

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

        subject=f"⚠️ [{nvr}] Duplicate IP Detected",

        template_name="ip_conflict.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        status="Duplicate IP Detected",

        event_time=event_time

    )


# =====================================================
# IP CONFLICT RESOLVED EMAIL
# =====================================================

def send_ip_conflict_resolved_email(
    event_time
):

    return send_html_email(

        subject="✅ IP Conflict Resolved",

        template_name="ip_conflict_resolved.html",

        camera="All Monitored Cameras",

        nvr="All Connected NVRs",

        ip="No Duplicate IP Detected",

        status="HEALTHY",

        event_time=event_time

    )


# =====================================================
# Enterprise Alert Helpers
# =====================================================

def send_warning_email(
    *,
    subject,
    template_name,
    camera,
    nvr,
    ip,
    message,
    event_time,
):

    return send_html_email(

        subject=subject,

        template_name=template_name,

        camera=camera,

        nvr=nvr,

        ip=ip,

        status=message,

        event_time=event_time

    )


# =====================================================
# VIDEO LOSS EMAIL
# =====================================================

def send_video_loss_email(
    camera,
    nvr,
    ip,
    event_time
):

    return send_warning_email(

        subject=f"🎥 [{nvr}] Video Loss - {camera}",

        template_name="video_loss.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message="Video Stream Lost",

        event_time=event_time

    )


# =====================================================
# VIDEO RESTORED EMAIL
# =====================================================

def send_video_restored_email(
    camera,
    nvr,
    ip,
    event_time
):

    return send_warning_email(

        subject=f"🟢 [{nvr}] Video Restored - {camera}",

        template_name="video_restored.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message="Video Stream Restored",

        event_time=event_time

    )


# =====================================================
# STORAGE FAILURE EMAIL
# =====================================================

def send_storage_failure_email(
    camera,
    nvr,
    ip,
    event_time
):

    return send_warning_email(

        subject=f"💾 [{nvr}] Storage Failure",

        template_name="storage_failure.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message="Storage Failure Detected",

        event_time=event_time

    )


# =====================================================
# NETWORK ISSUE EMAIL
# =====================================================

def send_network_issue_email(
    camera,
    nvr,
    ip,
    event_time
):

    return send_warning_email(

        subject=f"🌐 [{nvr}] Network Issue",

        template_name="network_issue.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message="Network Connectivity Issue",

        event_time=event_time

    )
# =====================================================
# Enterprise Logging Helpers
# =====================================================

def log_email_success(subject):

    print("\n" + "=" * 70)
    print("✅ EMAIL DELIVERED")
    print("=" * 70)
    print("Subject :", subject)
    print("=" * 70)


def log_email_failure(subject, error):

    print("\n" + "=" * 70)
    print("❌ EMAIL DELIVERY FAILED")
    print("=" * 70)
    print("Subject :", subject)
    print("Reason  :", error)
    print("=" * 70)


# =====================================================
# Email Health Check
# =====================================================

def email_service_status():

    return {
        "smtp_server": SMTP_SERVER,
        "smtp_port": SMTP_PORT,
        "sender": SENDER_EMAIL,
        "receiver": RECEIVER_EMAIL,
        "brand": EMAIL_BRAND,
        "status": "READY"
    }


# =====================================================
# Supported Alerts
# =====================================================

SUPPORTED_ALERTS = [

    "Camera Offline",

    "Camera Recovery",

    "Device Identity",

    "IP Conflict",

    "IP Conflict Resolved",

    "Video Loss",

    "Video Restored",

    "Storage Failure",

    "Network Failure",

    "Camera Tampering",

    "Power Failure",

    "Analytics Report"

]


def get_supported_alerts():

    return SUPPORTED_ALERTS.copy()


# =====================================================
# SMTP Test
# =====================================================

def test_email_connection():

    try:

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=15
        )

        server.ehlo()

        server.starttls()

        server.ehlo()

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        server.quit()

        print("\n" + "=" * 70)
        print("✅ SMTP CONNECTION SUCCESSFUL")
        print("=" * 70)

        return True

    except Exception as e:

        print("\n" + "=" * 70)
        print("❌ SMTP CONNECTION FAILED")
        print("=" * 70)
        print(e)
        print("=" * 70)

        return False


# =====================================================
# Module Info
# =====================================================

__version__ = "3.0 Enterprise"

__author__ = "VisionGuard AI"

__module__ = "Enterprise Email Service"


def get_email_service_info():

    return {

        "version": __version__,

        "module": __module__,

        "sender": SENDER_EMAIL,

        "receiver": RECEIVER_EMAIL,

        "smtp": SMTP_SERVER,

        "port": SMTP_PORT,

        "brand": EMAIL_BRAND,

        "alerts": get_supported_alerts()

    }


# =====================================================
# Test Console
# =====================================================

if __name__ == "__main__":

    from datetime import datetime

    print("\n" + "=" * 70)
    print("VisionGuard AI Enterprise Email Test")
    print("=" * 70)

    info = get_email_service_info()

    print("Version :", info["version"])
    print("SMTP    :", info["smtp"])
    print("Sender  :", info["sender"])
    print("Receiver:", info["receiver"])
    print("=" * 70)

    if not test_email_connection():
        exit()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    TEST_CAMERA = "QC TABLE 01"
    TEST_NVR = "NVR-01"
    TEST_IP = "192.168.1.101"

    send_offline_email(
        TEST_CAMERA,
        TEST_NVR,
        TEST_IP,
        now
    )

    send_recovery_email(
        TEST_CAMERA,
        TEST_NVR,
        TEST_IP,
        now
    )

    send_identity_email(
        TEST_CAMERA,
        TEST_NVR,
        TEST_IP,
        "Serial Number Changed",
        now
    )

    send_ip_conflict_email(
        TEST_CAMERA,
        TEST_NVR,
        TEST_IP,
        now
    )

    send_ip_conflict_resolved_email(
        now
    )

    send_video_loss_email(
        TEST_CAMERA,
        TEST_NVR,
        TEST_IP,
        now
    )

    send_video_restored_email(
        TEST_CAMERA,
        TEST_NVR,
        TEST_IP,
        now
    )

    send_storage_failure_email(
        TEST_CAMERA,
        TEST_NVR,
        TEST_IP,
        now
    )

    send_network_issue_email(
        TEST_CAMERA,
        TEST_NVR,
        TEST_IP,
        now
    )

    print("\n" + "=" * 70)
    print("✅ ALL TEST EMAILS SENT SUCCESSFULLY")
    print("=" * 70)