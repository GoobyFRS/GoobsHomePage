import os

import requests

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

UPTIME_KEY = os.getenv("UPTIME_KEY")


# =========================================================
# FETCH UPTIME-KUMA STATUS
# =========================================================

def fetch_uptime_status(config):
    """
    Fetch status information from Uptime-Kuma.

    Expected config structure:

    uptime_kuma:
      enabled: true
      api_url: "http://192.168.1.100:3001"
      status_page_slug: "homemc"
    """

    if not config.get("enabled", False):
        return {
            "online": False,
            "message": "Uptime-Kuma disabled",
            "services": []
        }

    try:
        api_url = config["api_url"]
        status_slug = config["status_page_slug"]

        headers = {
            "Authorization": f"Bearer {UPTIME_KEY}"
        }

        response = requests.get(
            f"{api_url}/api/status-page/{status_slug}",
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # =================================================
        # PARSE MONITORS
        # =================================================

        services = []

        #
        # Uptime-Kuma JSON structures vary slightly
        # between versions.
        #
        # This parser is intentionally defensive.
        #

        public_group_list = data.get("publicGroupList", [])

        for group in public_group_list:
            for monitor in group.get("monitorList", []):

                status = monitor.get("status", 0)

                services.append({
                    "name": monitor.get("name", "Unknown"),
                    "online": status == 1,
                    "ping": monitor.get("ping"),
                    "type": monitor.get("type", "unknown")
                })

        # =================================================
        # OVERALL STATUS
        # =================================================

        all_online = all(
            service["online"]
            for service in services
        ) if services else False

        return {
            "online": all_online,
            "message": (
                "All systems operational"
                if all_online
                else "Some services offline"
            ),
            "services": services
        }

    except Exception as error:
        return {
            "online": False,
            "message": f"Error: {error}",
            "services": []
        }