from gpiozero import Button
import time
import requests
import signal
import sys

URL = "http://10.3.1.120:8080/api/door-event"
HEADERS = {"Content-Type": "application/json"}

MODEM_URL = "http://127.0.0.1:5000/passCounts"

door = Button(
    17,
    pull_up=True,
    bounce_time=0.1
)

def send_event(event):
    payload = {
        "event": event,
        "timestamp": int(time.time() * 1000)
    }
    try:
        r = requests.post(URL, json=payload, headers=HEADERS, timeout=10)
        r.raise_for_status()
        print(f"Sent {event}")
        if r.headers.get("Content-Type", "").startswith("application/json"):
            print(r.json())
            
        if payload["event"] == "close":
            mr = requests.post(MODEM_URL, json=r.json(), headers=HEADERS, timeout=10)
    except Exception as e:
        print(f"Failed to send {event}: {e}")

def on_open():
    print("Door OPEN")
    send_event("open")

def on_close():
    print("Door CLOSED")
    send_event("close")

door.when_pressed = on_open
door.when_released = on_close

def shutdown(sig, frame):
    print("Exiting")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.pause()
