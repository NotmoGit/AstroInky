"""
handler.py — Button launcher and automatic refresh scheduler.

Button mapping:
  A short  → About screen       A long → Shutdown
  B short  → Solar system       B long → Astronomy picture of the day
  C short  → Stars & planets    C long → Moon facts
  D short  → Moon phase         D long → Instructions
"""

import os
import signal
import subprocess
import sys
import threading
import time
from signal import pause

from gpiozero import Button

# ── Script map ────────────────────────────────────────────────────────────────
SCRIPTS = {
    "a_short": "about.py",
    "a_long":  "shutdown.py",
    "b_short": "solar.py",
    "b_long":  "picture.py",
    "c_short": "stars.py",
    "c_long":  "othermoons.py",
    "d_short": "moon.py",
    "d_long":  "instructions.py",
}

DEFAULT_SCREEN   = "a_short"
REFRESH_INTERVAL = 3600  # seconds — refresh the current screen every 1 hour

# ── State ─────────────────────────────────────────────────────────────────────
current_process: subprocess.Popen | None = None
last_script_key: str = DEFAULT_SCREEN


# ── Process management ────────────────────────────────────────────────────────

def stop_current():
    global current_process
    if current_process and current_process.poll() is None:
        try:
            os.kill(current_process.pid, signal.SIGTERM)
            current_process.wait(timeout=5)
        except Exception as e:
            print(f"Warning: could not stop process: {e}")
    current_process = None


def run_script(key: str) -> None:
    global current_process, last_script_key
    last_script_key = key
    stop_current()
    print(f"→ Running {SCRIPTS[key]}")
    current_process = subprocess.Popen([sys.executable, SCRIPTS[key]])


def shutdown() -> None:
    print("Shutdown requested — displaying message then powering off.")
    stop_current()
    subprocess.run([sys.executable, SCRIPTS["a_long"]], check=True)
    subprocess.call("sudo shutdown -h now", shell=True)


# ── Auto-refresh thread ───────────────────────────────────────────────────────

def _refresh_loop() -> None:
    while True:
        time.sleep(REFRESH_INTERVAL)
        print(f"Auto-refreshing {SCRIPTS[last_script_key]}…")
        run_script(last_script_key)

# ── Buttons ───────────────────────────────────────────────────────────────────
button_a = Button(5,  hold_time=2)
button_b = Button(6,  hold_time=2)
button_c = Button(16, hold_time=2)
button_d = Button(24, hold_time=2)

button_a.when_pressed = lambda: run_script("a_short")
button_a.when_held    = shutdown

button_b.when_pressed = lambda: run_script("b_short")
button_b.when_held    = lambda: run_script("b_long")

button_c.when_pressed = lambda: run_script("c_short")
button_c.when_held    = lambda: run_script("c_long")

button_d.when_pressed = lambda: run_script("d_short")
button_d.when_held    = lambda: run_script("d_long")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("AstroPaper ready. Short press to switch screens, hold A to shutdown.")
    run_script(DEFAULT_SCREEN)
    threading.Thread(target=_refresh_loop, daemon=True).start()
    pause()
