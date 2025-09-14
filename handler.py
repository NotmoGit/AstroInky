from gpiozero import Button
from signal import pause
import subprocess
import os
import signal
import threading
import time
import sys
import configparser

# get config
config = configparser.ConfigParser()
config.read('config.ini')

# do we need to worry about a battery?
yes_words = ('y', 'Y','yes','Yes','YES',1,'true','True',True)
if config['global']['use_battery'] in yes_words:
  import ina219
  # Create an INA219 instance.
  ups_hat = ina219.ina219(addr=0x43)
  bus_voltage = ups_hat.getBusVoltage_V()             # voltage on V- (load side)
  current = ups_hat.getCurrent_mA()                   # current in mA
  power = ups_hat.getPower_W()                        # power in W
  p = (bus_voltage - 3)/1.2*100
  if(p > 100):p = 100
  if(p < 0):p = 0
  power_source = "mains"
  if(current < 0):
    power_source = "battery"

# default startup script
last_script_key = 'a_short'

# Define buttons with long press detection
button_a = Button(5, hold_time=2)
button_b = Button(6, hold_time=2)
button_c = Button(16, hold_time=2)
button_d = Button(24, hold_time=2)

# Define script paths
scripts = {
    'a_short': 'about.py',
    'a_long': 'shutdown.py',
    'b_short': 'solar.py',
    'b_long': 'picture.py',
    'c_short': 'stars.py',
    'c_long': 'othermoons.py',
    'd_short': 'moon.py',
    'd_long': 'instructions.py'
}

# Keep track of currently running script
current_process = None

def stop_current_script():
    global current_process
    if current_process and current_process.poll() is None:
        try:
            print(f"Stopping PID {current_process.pid}")
            os.kill(current_process.pid, signal.SIGTERM)
        except Exception as e:
            print(f"Failed to stop process: {e}")
    current_process = None

def run_script(script_key):
    global current_process, last_script_key
    last_script_key = script_key
    stop_current_script()
    print(f"Starting {scripts[script_key]}")
    current_process = subprocess.Popen([sys.executable, scripts[script_key]])

def shutdown_system(lowpower=False):
    if (lowpower == True):
      print("Battery is too low: Preparing to shut down...")
      stop_current_script()
      script = 'shutdown-lowpower.py'

    else:
      print("Long press on A: Preparing to shut down...")
      stop_current_script()
      script = scripts['a_long']

    print(f"Running shutdown script: {script}")

    try:
        # Run shutdown.py and wait for it to complete
        subprocess.run([sys.executable, script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Shutdown script failed: {e}")

    print("Shutdown script finished. Shutting down system now...")
    subprocess.call("sudo shutdown -h now", shell=True)


def hourly_refresher():
    global last_script_key
    while True:
        time.sleep(3600)  # wait 1 hour
        print("Refreshing current script...")
        run_script(last_script_key)

# Button bindings
button_a.when_pressed = lambda: run_script('a_short')
button_a.when_held = shutdown_system

button_b.when_pressed = lambda: run_script('b_short')
button_b.when_held = lambda: run_script('b_long')

button_c.when_pressed = lambda: run_script('c_short')
button_c.when_held = lambda: run_script('c_long')

button_d.when_pressed = lambda: run_script('d_short')
button_d.when_held = lambda: run_script('d_long')

if __name__ == "__main__":
    print("Button launcher active. Short presses switch scripts. Hold About to shutdown.")
    run_script('d_long')
    threading.Thread(target=hourly_refresher, daemon=True).start()
    if config['global']['use_battery'] in yes_words:
      # Check battery status
      while True:
        current = ups_hat.getCurrent_mA()
        bus_voltage = ups_hat.getBusVoltage_V()
        p = (bus_voltage - 3)/1.2*100
        if (power_source == "mains" and current < 0):
          # We were on mains power when we started but current is now negative
          # Something has changed so refresh the screen
          print("We have changed to battery power, reloading script")
          run_script(last_script_key)
          power_source = "battery"
        elif (power_source == "battery" and current > 0):
          print("We have changed to mains power, reloading script")
          # We were on battery power but now current is positive
          # Something has changed so refresh the screen
          run_script(last_script_key)
          power_source = "mains"
        if (int(p) < 5):
          print("Power is too low, shutting down")
          # Battery percentage is below 5%
          shutdown_system(lowpower=True)
        time.sleep(10)
    else:
      pause()
