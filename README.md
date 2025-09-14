# 🌙 Inky Impression Moon Phase Display

A Python project for Raspberry Pi that displays various astronomical information pages on a **6-color Inky Impression e-ink display**, using **PyEphem** for precise astronomical calculations.

This project was forked from the great starting point (with all the difficult maths already done) here: https://github.com/NotmoGit/AstroInky

## ✨ Features

- Button-driven interface using the Inky Impression’s 4 hardware buttons
- Shows the current **moon phase** as an image, as well as:
  - Moonrise & moonset times
  - Azimuth and altitude of the moon (based on a configurable latitude/longitude)
- Displays **visible stars and planets** (updates on refresh)
- Renders an accurate visual representation of the **solar system** with the planets in their approximate current positions
- Shows an **"About"** page with a personal message
- Supports the Waveshare UPS HAT to make AstroInky portable
- Supports the Pimoroni GPS breakout to allow AstroInky to set itself up automatically

### Long Button Press Functions

- Pulls a **random NASA Astronomy Picture of the Day** (with title and description)
- Displays a **random named moon** of a planet with fun facts
- **Shuts the system down** and displays a shutdown message
- Shows an **"Instructions"** page

> Everything is designed to be displayed in **portrait** orientation (not landscape)

---

## 🔧 Hardware Requirements

- Raspberry Pi (any model with GPIO support)
- [Inky Impression (7-color, 5.7")](https://shop.pimoroni.com/products/inky-impression-5-7)
- SD card, power supply, and network access for the Pi
- Optionally, the Waveshare UPS HAT
- Optionally, the Pimoroni GPS breakout

---

## 🧰 Software Requirements and Dependencies

- Python 3.7+
- [PyEphem](https://pypi.org/project/ephem/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Pimoroni Inky library](https://github.com/pimoroni/inky/)
- `gpiozero`

---
## Installation

- See SETUP.md for instructions
---
## ▶️ Usage

A `systemd` service runs on startup, activates a virtual environment, and executes `handler.py` (which in turn launches `about.py` as the startup screen).

Long-pressing the **A** button (which, unintuitively, is on the right side) will **shut down** the system and display a shutdown message.

---

## ⚙️ Customising

- **Location, NASA API, Custom Messages** are all set in config.ini
- Hardware support is also set in config.ini
---

## 🛠️ To Do

- Create a centralized positioning/layout system
- Fix all the commenting

## 🖨️ 3D Printed Case

- Three part (OK, 4 if you count the legs seperately... OK, 8 if you also count the buttons seperately...) 3D printed case
- Printed in PLA with default settings - you will need supports for the back piece
- Uses 4 x M2.5mm bolts that screw into the Inky Impression - I used some filed down standoffs to make everything a bit more rigid but it probably isn't needed
- Uses 4 x M2 bolts and nuts to hold the front face on
- STL files:
  - [Printables: Inky Impression Spectra 7.3 Case](https://www.printables.com/model/1363758-inky-impression-spectra-73-case)
  - [MakerWorld: Inky Impression Spectra 7.3 Case](https://makerworld.com/en/models/1634076-inky-impression-spectra-7-3-case)

