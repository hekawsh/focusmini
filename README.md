# Focus Mini (Python)

<p align="center">
  <img src="https://github.com/user-attachments/assets/a29ffd4a-16ca-41df-ad68-d4fee3d19295 "width="49%" />
  <img src="https://github.com/user-attachments/assets/117b07ff-749b-4f9c-9a88-cad9302a55e9 "width="49%" />
</p>

## Acknowledgements

Complete code is generated using Artifical Intelligence ([DeepSeek](https://deepseek.com))

## Beta Feature: History

Just in case to register the "environmental balance" and the average is calculated above the entries.

## How to use

### Download
You can download focusmini.exe from releases. If it isn't allowed by browser, then use the below method.

### Build from source

0. Download [Python](https://www.python.org/downloads/) and follow the steps to install pythonCLI.
1. Download focusmini.py from release.
2. Ctrl + Right Click in the same folder, anad select "Open Powershell Window Here."
3. Copy & Paste following commands one by one:
   ```Powershell
   pip install flet sounddevice numpy
   pip install pyinstaller
   python -m PyInstaller --onefile --windowed --name "FocusMini" --hidden-import sounddevice --hidden-import numpy --collect-data flet focusmini.py
   ```
4. Wait until it's built, and the .exe will be inside the `dist` folder in the same directory.

Designed to help you stay out of flow and remain aware of time passing – entirely crafted with artificial intelligence.
