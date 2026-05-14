import requests
import yaml

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template

from services.weather import fetch_weather
from services.uptime import fetch_uptime_status

# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

# =========================================================
# YAML LOADERS
# =========================================================

def load_data():
    with open("data.yml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_nav_menu():
    with open("static/nav_menu.yml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


# =========================================================
# UPTIME-KUMA STATUS
# =========================================================

def fetch_uptime_status(config):
    """
    Fetch status from Uptime-Kuma.

    This assumes:
    - Uptime-Kuma API is enabled
    - You have an API key
    - Your status page is publicly accessible
    """

    if not config.get("enabled", False):
        return {
            "online": False,
            "message": "Uptime-Kuma disabled"
        }

    try:
        api_url = config["api_url"]

        headers = {
            "Authorization": f"Bearer {UPTIME_KEY}"
        }

        response = requests.get(
            f"{api_url}/api/status-page/{config['status_page_slug']}",
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # Placeholder parsing logic
        #
        # You may later want:
        # - monitor list
        # - ping
        # - status mapping
        # - service summaries

        return {
            "online": True,
            "message": "All systems operational",
            "raw": data
        }

    except Exception as error:
        return {
            "online": False,
            "message": f"Error: {error}"
        }


# =========================================================
# MAIN ROUTE
# =========================================================

@app.route("/")
def index():
    data = load_data()

    nav_menu = load_nav_menu()

    # =====================================================
    # CLOCKS
    # =====================================================

    clocks = []

    for item in data["clocks"]:
        now = datetime.now(
            ZoneInfo(item["timezone"])
        )

        clocks.append({
            "label": item["label"],
            "time": now.strftime("%I:%M:%S %p"),
            "date": now.strftime("%A, %B %d")
        })

    # =====================================================
    # WEATHER
    # =====================================================

    weather_data = []

    for location in data["weather"]["locations"]:
        weather = fetch_weather(
            location["latitude"],
            location["longitude"]
        )

        weather_data.append({
            "label": location["label"],
            "temperature": weather["current_temp"],
            "condition": (
                f"H {weather['high']}° "
                f"L {weather['low']}°"
            ),
            "wind": (
                f"{weather['wind_speed']} MPH "
                f"{weather['wind_direction']}"
            )
        })

    # =====================================================
    # UPTIME-KUMA
    # =====================================================

    uptime_status = fetch_uptime_status(
        data["uptime_kuma"]
    )

    # =====================================================
    # TEMPLATE RENDER
    # =====================================================

    return render_template(
        "index.html",
        site=data["site"],
        appearance=data["appearance"],
        clocks=clocks,
        weather_data=weather_data,
        uptime_status=uptime_status,
        schedule=data["schedule"],
        nav_menu=nav_menu["items"]
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )