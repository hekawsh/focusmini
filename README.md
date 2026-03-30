# 🎧 Focus Mini

<div style="display: flex; gap: 10px; justify-content: center;">
  <img width="270" height="258" alt="image (23)" src="https://github.com/user-attachments/assets/a29ffd4a-16ca-41df-ad68-d4fee3d19295" />
  <img width="270" height="258" alt="image (24)" src="https://github.com/user-attachments/assets/117b07ff-749b-4f9c-9a88-cad9302a55e9" />
</div>

**Focus Mini** is a minimalist desktop ticker that blends a clean, precise tick (every 5 seconds) with a continuous background of **white noise**.  
It helps you *stay out of flow* – allowing you to sense time passing and remain aware of the present moment, all with the assistance of artificial intelligence.

## ✨ Features

- **Adjustable Balance** – Drag the central slider from `100% Tick / 0% Noise` to `0% Tick / 100% White Noise`.
- **Steady Tick** – The tick occurs every 5 seconds, aligned to real‑time seconds (`Δt = 5s`).
- **Session History** – Every time you stop a session, your chosen balance is saved with a timestamp.
- **Personalised Recommendation** – The History tab shows the average balance from all your recorded sessions.
- **Portable App** – Download a single `.exe` file (Windows) – no Python installation required.
- **Clean, Modern UI** – Simple Material You design, spacebar toggles start/stop, and a non‑resizable window.

## 🖥️ Download & Install (no Python needed)

1. Go to the **[Releases](https://github.com/hekawsh/focusmini/releases)** page.
2. Download the latest `FocusMini.exe` file.
3. Double‑click the downloaded file – no installation required. Run it from any folder or USB drive.

## ⌨️ How to Use

1. **Adjust the balance** – move the slider left (more white noise) or right (more tick).
2. **Start / Stop** – click the **Start** or **Stop** button, or simply press the **spacebar**.
3. **View your history** – click the **History** tab to see past sessions and your recommended balance.
4. **Delete entries** – remove individual sessions from the history list using the trash icon.

## 👨‍💻 Running from Source (for developers)

If you want to run the Python script directly (e.g., to modify or debug), follow these steps.

### Prerequisites

- Python 3.7 or higher
- Git (optional, to clone the repository)

### Installation & Setup

```bash
# Clone the repository (or download the source code)
git clone https://github.com/hekawsh/focusmini.git
cd focusmini

# Install the required Python packages
pip install flet sounddevice numpy

# Run the app
python focusmini.py
```

## 📦 Creating Your Own Executable

If you change the source code and want to build a fresh `.exe` file:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "FocusMini" --hidden-import sounddevice --hidden-import numpy --collect-data flet focusmini.py
```

The new executable will be inside the `dist` folder.

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Built with the [Flet](https://flet.dev) framework.
- Audio playback powered by `sounddevice` and `numpy`.
- **Code, documentation, and assistance** generated with the help of [DeepSeek](https://deepseek.com), an AI assistant by DeepSeek Company.
- Designed to help you *stay out of flow* and remain aware of time passing – entirely crafted with artificial intelligence.
```
