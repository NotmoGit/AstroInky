# 🌙 Inky Impression Moon Phase Display

A Python project for Raspberry Pi that displays various astronomical information pages on a **6-color Inky Impression e-ink display**, using **PyEphem** for precise astronomical calculations.

This is currently not a particularly easy project to customise - mainly because this is my first real python/Inky project and I didn't write it with other people using it in mind. However, it is possible if you follow the steps in the Customising section

AI (ChatGPT/Claude) was used fairly extensively to write and debug and, as such, the commenting can be a bit sporadic and inconsistent. This was a learning project, not just "vibe-coded".

---

## ✨ Features

**Short press functions:**
- Current **moon phase** image with phase name, moonrise & moonset times, and azimuth/altitude
- Visual **solar system diagram** with all eight planets in their approximate current positions
- List of currently **visible stars and planets** with magnitude, altitude, and azimuth
- **About** page with a personal message

**Long press functions:**
- Random **NASA Astronomy Picture of the Day** with title and description
- Random **named moon** of a solar system planet with facts
- **Instructions** page showing the button map
- **Shutdown** — displays a message and powers the Pi off safely

> Everything is designed to display in **portrait** orientation.

---

## 🔧 Hardware

| Component | Details |
|---|---|
| Computer | Raspberry Pi Zero W |
| Display | [Pimoroni Inky Impression Spectra 7.3 (6-colour e-ink)](https://shop.pimoroni.com/products/inky-impression-7-3) |
| Storage | microSD card, 8GB minimum |
| Power | 5V micro-USB |

The Inky Impression connects directly to the Pi's 40-pin GPIO header. No soldering required.

---

## 🗂️ Project Structure

```
AstroInky/
├── config.py           # All settings — location, paths, font sizes, API key
├── display_utils.py    # Shared display setup: colours, fonts, nav bar, show()
├── astro_utils.py      # Shared astronomy helpers: observer, moon phase, time
├── handler.py          # Button handler and auto-refresh scheduler
│
├── moon.py             # Moon phase screen
├── solar.py            # Solar system diagram screen
├── stars.py            # Stars and planets screen
├── othermoons.py       # Random moon facts screen
├── picture.py          # NASA Astronomy Picture of the Day screen
├── about.py            # About / birthday message screen
├── instructions.py     # Button reference screen
├── shutdown.py         # Shutdown confirmation screen
│
├── fonts/
│   └── Merriweather-VariableFont_opsz,wdth,wght.ttf
├── icons/              # SVG navigation and data icons
├── phases/             # Moon phase PNG images
├── pics/               # Local photos
├── moons.json          # Solar system moon facts database
├── creds.txt           # NASA API key (do not commit this)
└── face.jpg            # Photo shown on instructions screen
```

---

## 🕹️ Button Map

The display sits in portrait orientation. Buttons run left to right across the bottom edge. Note that **Button A is on the right**, which is counterintuitive.

| Button | Short Press | Long Press (hold 2s) |
|---|---|---|
| D (leftmost) | Moon phase | Instructions |
| C | Stars & planets | Moon facts |
| B | Solar system | Astronomy picture |
| A (rightmost) | About screen | **Shutdown** |

The display auto-refreshes the current screen every hour.

---

## 🧰 Dependencies

| Package | Purpose |
|---|---|
| `inky[rpi]` | Pimoroni Inky Impression display driver |
| `Pillow` | Image composition and drawing |
| `ephem` | Astronomical calculations |
| `cairosvg` | SVG icon rendering |
| `gpiozero` | Button input via GPIO |
| `requests` | NASA APOD API calls |

---

## ▶️ Installation

### 1. Flash the SD card

Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and flash **Raspberry Pi OS Lite (32-bit)** to your SD card. In the Imager settings (gear icon), configure:

- Hostname: `astroInky` (or whatever you prefer)
- Enable SSH
- Your WiFi credentials
- Timezone: your local timezone

### 2. Boot and connect

Insert the SD card, power on the Pi, wait ~90 seconds, then SSH in:

```bash
ssh youruser@astroInky.local
```

### 3. Update the system

```bash
sudo apt update && sudo apt upgrade -y
```

### 4. Enable SPI and I2C

```bash
sudo raspi-config
```

Navigate to **Interface Options** and enable both **SPI** and **I2C**. Reboot when prompted.

### 5. Fix the SPI chip-select conflict

The Inky library needs to manage the SPI chip select pin itself. Edit the boot config:

```bash
sudo nano /boot/firmware/config.txt
```

> On older Pi OS versions this may be `/boot/config.txt` instead.

Replace `dtparam=spi=on` with:

```
dtoverlay=spi0-0cs
```

Reboot.

### 6. Install system dependencies

```bash
sudo apt install -y \
  python3-pip \
  python3-pil \
  libcairo2-dev \
  libffi-dev \
  libjpeg-dev \
  libopenjp2-7 \
  i2c-tools
```

### 7. Transfer project files

Run this from your computer in the folder containing the project:

```bash
scp -r AstroInky youruser@astroInky.local:/home/youruser/
```

### 8. Add your NASA API key

Create `creds.txt` in the project folder containing just your key:

```bash
echo "YOUR_NASA_API_KEY" > /home/youruser/AstroInky/creds.txt
```

Get a free key at [api.nasa.gov](https://api.nasa.gov/).

### 9. Install Python packages

```bash
pip3 install inky[rpi] pillow cairosvg ephem requests gpiozero --break-system-packages
```

### 10. Test it

```bash
cd /home/youruser/AstroInky
python3 moon.py
```

The display should update with the current moon phase.

### 11. Autostart on boot

Create a systemd service:

```bash
sudo nano /etc/systemd/system/astroInky.service
```

Paste (updating the username and path):

```ini
[Unit]
Description=AstroInky Display
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/youruser/AstroInky/handler.py
WorkingDirectory=/home/youruser/AstroInky
User=youruser
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable astroInky
sudo systemctl start astroInky
```

---

## ⚙️ Customising

All the settings you're likely to want to change are in `config.py` — you shouldn't need to touch any other file for basic customisation.

```python
# Your location
LATITUDE   = "38.8977"
LONGITUDE  = "77.03 65"
ELEVATION  = 15
TIMEZONE   = "Europe/London"
UTC_OFFSET = 0

# Font sizes
FONT_SIZE       = 18
FONT_SIZE_LARGE = 24
```

## 🛠️ To Do

- Commenting is still inconsistent across files
- The `stars.py` screen can overflow if many objects are visible simultaneously — a scroll or truncation mechanism would help
- The solar system diagram orbit radii are hand-tuned for this specific display size and may need adjustment for other Inky models

## 🖨️ 3D Printed Case

- Three part (OK, 4 if you count the legs seperately... OK, 8 if you also count the buttons seperately...) 3D printed case
- Printed in PLA with default settings - you will need supports for the back piece
- Uses 4 x M2.5mm bolts that screw into the Inky Impression - I used some filed down standoffs to make everything a bit more rigid but it probably isn't needed
- Uses 4 x M2 bolts and nuts to hold the front face on
- STL files:
  - [Printables: Inky Impression Spectra 7.3 Case](https://www.printables.com/model/1363758-inky-impression-spectra-73-case)
  - [MakerWorld: Inky Impression Spectra 7.3 Case](https://makerworld.com/en/models/1634076-inky-impression-spectra-7-3-case)


## 🔭 Astronomical Data

All positions and times are calculated locally using [PyEphem](https://rhodesmill.org/pyephem/). All times displayed are in local time (configured in `config.py`). Moon phase and moonrise/moonset accuracy has been verified against [timeanddate.com](https://www.timeanddate.com) and independent calculators.

---

## 📄 Credits

- Astronomy calculations — [PyEphem](https://rhodesmill.org/pyephem/)
- Space images — [NASA APOD API](https://api.nasa.gov/)
- Font — [Merriweather](https://fonts.google.com/specimen/Merriweather) (Google Fonts, OFL licence)
- Icons — custom SVG
