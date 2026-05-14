from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template
import yaml

app = Flask(__name__)


def load_data():
    with open("data.yml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@app.route("/")
def index():
    data = load_data()

    clocks = []

    for item in data["clocks"]:
        now = datetime.now(ZoneInfo(item["timezone"]))

        clocks.append({
            "label": item["label"],
            "time": now.strftime("%I:%M:%S %p"),
            "date": now.strftime("%A, %B %d")
        })

    weather_data = []

    for location in data["weather"]["locations"]:
        weather_data.append({
            "label": location["label"],
            "temperature": "--",
            "condition": "Placeholder"
        })

    uptime_status = {
        "online": True,
        "message": "Placeholder status"
    }

    return render_template(
        "index.html",
        site=data["site"],
        appearance=data["appearance"],
        clocks=clocks,
        weather_data=weather_data,
        uptime_status=uptime_status,
        schedule=data["schedule"]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)