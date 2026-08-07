import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import EMAIL_BRAND

# =====================================================
# VisionGuard AI Enterprise Email Service v4.0
# =====================================================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "Zubair.khan@1mg.com"
APP_PASSWORD = "garajkqynquqccpe"

RECEIVER_EMAIL = "Zubair.khan@1mg.com"

TEMPLATE_DIR = Path(__file__).parent / "templates"

# =====================================================
# Template Renderer
# =====================================================

def render_template(template_name: str, data: dict):

    template_path = TEMPLATE_DIR / template_name

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    for key, value in data.items():
        html = html.replace(
            "{{" + key + "}}",
            str(value)
        )

    return html


# =====================================================
# Enterprise Logger
# =====================================================

def log_email_success(subject):

    print("\n" + "=" * 70)
    print("✅ EMAIL SENT")
    print("=" * 70)
    print(subject)
    print("=" * 70)


def log_email_failure(subject, error):

    print("\n" + "=" * 70)
    print("❌ EMAIL FAILED")
    print("=" * 70)
    print(subject)
    print(error)
    print("=" * 70)
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
            }
        )

        msg = MIMEMultipart("alternative")
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject

        msg.attach(
            MIMEText(
                html,
                "html",
                "utf-8"
            )
        )

        print("========== EMAIL DEBUG ==========")
        print("Subject :", subject)
        print("Template:", template_name)
        print("From    :", SENDER_EMAIL)
        print("To      :", RECEIVER_EMAIL)

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=20
        ) as server:

            server.ehlo()

            server.starttls()

            server.ehlo()

            print("TLS OK")

            server.login(
                SENDER_EMAIL,
                APP_PASSWORD
            )

            print("LOGIN SUCCESS")

            server.sendmail(
                SENDER_EMAIL,
                RECEIVER_EMAIL,
                msg.as_string()
            )

            print("MAIL SENT SUCCESSFULLY")

        log_email_success(subject)

        return True

    except Exception as e:

        log_email_failure(
            subject,
            e
        )

        return False


# =====================================================
# Generic Warning Email
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
# CAMERA OFFLINE EMAIL
# =====================================================

def send_offline_email(
    camera,
    nvr,
    ip,
    event_time
):

    return send_warning_email(

        subject=f"🔴 [{nvr}] Camera Offline - {camera}",

        template_name="offline.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message="Camera is Offline",

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

    return send_warning_email(

        subject=f"🟢 [{nvr}] Camera Recovered - {camera}",

        template_name="recovery.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message="Camera Restored Successfully",

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

    return send_warning_email(

        subject=f"🚨 [{nvr}] Device Identity Changed - {camera}",

        template_name="identity.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message=issues,

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

    return send_warning_email(

        subject=f"⚠️ [{nvr}] Duplicate IP Detected",

        template_name="ip_conflict.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message="Duplicate IP Detected",

        event_time=event_time

    )


# =====================================================
# IP CONFLICT RESOLVED EMAIL
# =====================================================

def send_ip_conflict_resolved_email(
    event_time
):

    return send_warning_email(

        subject="✅ IP Conflict Resolved",

        template_name="ip_conflict_resolved.html",

        camera="All Monitored Cameras",

        nvr="All Connected NVRs",

        ip="-",

        message="No Duplicate IP Detected",

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
# RECORDING LOSS EMAIL
# =====================================================


def send_recording_loss_email(
    camera,
    nvr,
    ip,
    loss_from,
    loss_to,
    duration,
):

    print("######## send_recording_loss_email CALLED ########")

    return send_warning_email(
        subject=f"⛔ [{nvr}] Recording Loss - {camera}",
        template_name="video_loss.html",
        camera=camera,
        nvr=nvr,
        ip=ip,
        message=(
            f"Recording Interrupted\n\n"
            f"Missing From : {loss_from}\n"
            f"Missing To   : {loss_to}\n"
            f"Duration     : {duration}"
        ),
        event_time=loss_from,
    )


# =====================================================
# RECORDING RECOVERY EMAIL
# =====================================================

def send_recording_recovery_email(
    camera,
    nvr,
    ip,
    loss_from,
    loss_to,
    restored_at,
    duration,
):

    return send_warning_email(

        subject=f"✅ [{nvr}] Recording Restored - {camera}",

        template_name="video_restored.html",

        camera=camera,

        nvr=nvr,

        ip=ip,

        message=(
            f"Recording Restored\n\n"
            f"Loss From : {loss_from}\n"
            f"Loss To   : {loss_to}\n"
            f"Recovered : {restored_at}\n"
            f"Duration  : {duration}"
        ),

        event_time=restored_at

    )
