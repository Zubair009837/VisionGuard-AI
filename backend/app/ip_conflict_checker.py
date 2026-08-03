from collections import defaultdict
from datetime import datetime

from .email_service import send_ip_conflict_email


def check_ip_conflicts(cameras):
    ip_map = defaultdict(list)

    for camera in cameras:
        ip = camera.get("ip", "").strip()

        if ip:
            ip_map[ip].append(camera)

    conflicts = []

    for ip, devices in ip_map.items():
        if len(devices) > 1:
            conflicts.append({
                "ip": ip,
                "devices": devices
            })

    return conflicts


def print_conflicts(conflicts):

    if not conflicts:
        return

    print("\n" + "=" * 70)
    print("🚨 IP CONFLICT DETECTED")
    print("=" * 70)

    for conflict in conflicts:

        print(f"\nDuplicate IP : {conflict['ip']}")
        print("-" * 70)

        for camera in conflict["devices"]:

            print(
                f"{camera['nvr']} | "
                f"{camera['name']} | "
                f"{camera['status']}"
            )

            event_time = datetime.now().strftime("%d %b %Y %I:%M:%S %p")

            send_ip_conflict_email(
                camera=camera["name"],
                nvr=camera["nvr"],
                ip=camera["ip"],
                event_time=event_time
            )

    print("=" * 70)