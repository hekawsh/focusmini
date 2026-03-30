# 🎧 Focus Mini

**Focus Mini** is a minimalist desktop focus timer that blends a clean, precise tick (every 5 seconds) with a continuous background of **white noise**.  
It helps you maintain concentration during deep work sessions by letting you adjust the balance between rhythm and ambient sound.

> *This software and its README were generated with the help of [DeepSeek](https://deepseek.com), an AI assistant.*

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
