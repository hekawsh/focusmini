import flet as ft
import threading
import time
import math
import random
import numpy as np
import sounddevice as sd
import pystray
import win32event
import win32api
import win32gui
import win32con
import winerror
from PIL import Image, ImageDraw
import sys
import os

# Mutex for single instance
mutex_name = "FocusMini-{F1A2B3C4-D5E6-4789-A0B1-C2D3E4F5A6B7}"
mutex = win32event.CreateMutex(None, False, mutex_name)
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    hwnd = win32gui.FindWindow(None, "Focus Mini")
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    sys.exit(0)

class Player:
    def __init__(self, mix):
        self.interval = 5.0
        self.rate = 44100
        self.tick_len = 0.05
        self.tick_freq = 1000
        self.tick_amp = mix / 100.0
        self.noise_amp = (100 - mix) / 100.0
        self.tick_wave = self._tick()
        self.tick_samples = len(self.tick_wave)
        self.tick_playing = False
        self.tick_pos = 0
        self.stream = None
        self.stop = threading.Event()
        self.tick_needed = False
        self.cur_tick_amp = self.tick_amp
        self.cur_noise_amp = self.noise_amp

    def _tick(self):
        n = int(self.rate * self.tick_len)
        t = np.linspace(0, self.tick_len, n, False)
        w = np.sin(2 * np.pi * self.tick_freq * t)
        env = np.exp(-5 * t / self.tick_len)
        w = w * env
        w = w / (np.max(np.abs(w)) if np.max(np.abs(w)) > 0 else 1)
        return w.astype(np.float32)

    def set_mix(self, mix):
        self.cur_tick_amp = mix / 100.0
        self.cur_noise_amp = (100 - mix) / 100.0

    def _sched(self):
        nxt = math.ceil(time.time() / self.interval) * self.interval
        while not self.stop.is_set():
            wait = nxt - time.time()
            if wait > 0: time.sleep(wait)
            if self.stop.is_set(): break
            self.tick_needed = True
            nxt += self.interval

    def _audio(self, outdata, frames, info, status):
        if self.tick_needed and not self.tick_playing:
            self.tick_playing = True
            self.tick_pos = 0
            self.tick_needed = False
        outdata[:] = 0.0
        for i in range(frames):
            n = random.uniform(-1.0, 1.0)
            t = 0.0
            if self.tick_playing:
                if self.tick_pos < self.tick_samples:
                    t = self.tick_wave[self.tick_pos]
                    self.tick_pos += 1
                else:
                    self.tick_playing = False
            outdata[i] = self.cur_noise_amp * n + self.cur_tick_amp * t

    def start(self):
        self.stream = sd.OutputStream(samplerate=self.rate, channels=1, callback=self._audio)
        self.stream.start()
        self.sched = threading.Thread(target=self._sched, daemon=True)
        self.sched.start()

    def stop_audio(self):
        self.stop.set()
        if self.stream:
            self.stream.stop()
            self.stream.close()

class TrayApp:
    def __init__(self, page):
        self.page = page
        self.icon = None

    def get_icon_image(self):
        if os.path.exists("icon.ico"):
            return Image.open("icon.ico")
        img = Image.new('RGB', (64, 64), (66, 133, 244))
        d = ImageDraw.Draw(img)
        d.ellipse((8, 8, 56, 56), fill=(255, 255, 255))
        return img

    def run(self):
        img = self.get_icon_image()
        def on_click(icon, item):
            if str(item) == "Show":
                self.page.run_thread(self.restore_window)
            elif str(item) == "Exit":
                self.page.run_thread(self.page.stop_all)
                icon.stop()
        menu = pystray.Menu(pystray.MenuItem("Show", on_click), pystray.MenuItem("Exit", on_click))
        self.icon = pystray.Icon("FocusMini", img, "Focus Mini", menu)
        self.icon.run()

    def restore_window(self):
        self.page.window.visible = True
        self.page.window.minimized = False
        self.page.update()
        hwnd = win32gui.FindWindow(None, "Focus Mini")
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)

def main(page: ft.Page):
    page.title = "Focus Mini"
    page.window.width, page.window.height = 440, 520
    page.window.resizable = False

    if os.path.exists("icon.ico"):
        page.window.icon = "icon.ico"

    tray_app = TrayApp(page)

    def hide_to_tray(e):
        page.window.visible = False
        page.update()
        if not hasattr(page, "tray_thread_started"):
            page.tray_thread_started = True
            threading.Thread(target=tray_app.run, daemon=True).start()

    page.on_close = hide_to_tray

    blue = ft.Colors.BLUE_400
    slider = ft.Slider(min=0, max=100, divisions=20, value=100,
                       active_color=blue, width=220)
    # Slider label update (live)
    slider.on_change = lambda e: update_mix()

    start_btn = ft.Button("Start", icon=ft.Icons.PLAY_ARROW, on_click=lambda _: on_start(),
                          style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=blue))
    stop_btn = ft.Button("Stop", icon=ft.Icons.STOP, visible=False, on_click=lambda _: on_stop(),
                         style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_500))
    status = ft.Text("Ready", size=14)

    page.add(
        ft.Column([
            ft.Row([ft.Icon(ft.Icons.TIMER, color=blue, size=32),
                    ft.Text("Focus Mini", size=28, weight="bold", color=blue)], alignment="center"),
            ft.Divider(),
            ft.Row([ft.Text("Noise", weight="bold"), slider, ft.Text("Tick", weight="bold")], alignment="center"),
            ft.Divider(),
            ft.Row([start_btn, stop_btn], alignment="center"),
            status,
            ft.Button("Hide to Tray", icon=ft.Icons.HIDE_IMAGE, on_click=hide_to_tray),
            ft.Divider(),
            ft.Text("Collaborative AI Build", size=11, color=ft.Colors.GREY_400),
            ft.Text("Credits: DeepSeek, Gemini, and the Developer", size=10, color=ft.Colors.GREY_500),
            ft.TextButton("GitHub Source", url="https://github.com/hekawsh/focusmini")
        ], horizontal_alignment="center", spacing=15)
    )

    running, session = False, None

    def update_mix():
        nonlocal session
        if running and session:
            session.set_mix(int(slider.value))

    def on_start():
        nonlocal running, session
        if running:
            return
        mix_val = int(slider.value)
        session = Player(mix_val)
        session.start()
        start_btn.visible, stop_btn.visible, status.value, status.color = False, True, "Running", ft.Colors.GREEN_500
        running = True
        page.update()

    def on_stop():
        nonlocal running, session
        if not running:
            return
        if session:
            session.stop_audio()
            session = None
        start_btn.visible, stop_btn.visible, status.value, status.color = True, False, "Stopped", ft.Colors.RED_500
        running = False
        page.update()

    def toggle_playback(e: ft.KeyboardEvent):
        if e.key == " ":
            if running:
                on_stop()
            else:
                on_start()

    page.on_keyboard_event = toggle_playback

    page.stop_all = lambda: (on_stop(), page.window.close(), sys.exit(0))

ft.run(main)