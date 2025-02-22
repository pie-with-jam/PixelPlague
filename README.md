# PixelPlague
[Project Description](#project-description) - [Key Features](#key-features) - [Tech Stack](#technology-stack) - [Installation Instructions](#installation-instructions)

## Project Description

This project creates the effect of flickering, artefacts and random text on the screen, and periodically rotates the screen 90 degrees. The programme uses Win32 API to interact with the screen and create graphic effects.

## Key Features

- **Flicker Effect**: Random coloured rectangles appear on the screen.
- **Artefacts**: Additional visual artefacts are created around the flicker.
- **Random Text**: Milk text appears periodically on the screen with different sizes and colours.
- **Screen Rotation**: The screen rotates 90 degrees every 5-7 seconds.
- **Scaling support**: The programme works correctly on screens with scaling (e.g. 125%, 150%).

## Tech Stack

**Programming Language:** Python 3

**Libraries:**

The following libraries are required to run the programme:
- `pywin32` (for working with Win32 API)
- `ctypes` (for obtaining DPI and scaling)

**Tools:**

- **IDE/Editor:** PyCharm
- **Version Control:** Git

**Platform:** Windows

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/pie-with-jam/PixelPlague.git
   ```

2. Navigate into the project directory:
   ```bash
   cd PixelPlague
   ```

3. Install the necessary dependencies:
   ```bash
   pip install -r .\requirements.txt
   ```

4. Build the executable using PyInstaller:
   ```bash
   pyinstaller .\PixelPlague.spec
   ```

   This will create a standalone executable that you can run without needing to install Python.