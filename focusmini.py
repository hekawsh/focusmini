import flet as ft
import threading
import time
import math
import random
import numpy as np
import sounddevice as sd
import sys
import json
import os
from datetime import datetime

# ------------------------------------------------------------
# Audio engine – white noise + tick (Δt = 5s)
# ------------------------------------------------------------
class TickNoiseFocus:
    def __init__(self, balance_percent):
        self.interval = 5.0
        self.balance = balance_percent

        self.sample_rate = 44100
        self.tick_duration = 0.05
        self.tick_freq = 1000

        self.tick_amp = balance_percent / 100.0
        self.noise_amp = (100 - balance_percent) / 100.0

        self.tick_wave = self._generate_tick_wave()
        self.tick_samples = len(self.tick_wave)

        self.tick_playing = False
        self.tick_offset = 0
        self.stream = None
        self.stop_event = threading.Event()
        self.tick_requested = False

        self.current_tick_amp = self.tick_amp
        self.current_noise_amp = self.noise_amp
        self.scheduler_thread = None

    def _generate_tick_wave(self):
        num_samples = int(self.sample_rate * self.tick_duration)
        t = np.linspace(0, self.tick_duration, num_samples, endpoint=False)
        wave = np.sin(2 * np.pi * self.tick_freq * t)
        envelope = np.exp(-5 * t / self.tick_duration)
        wave = wave * envelope
        wave = wave / np.max(np.abs(wave))
        return wave.astype(np.float32)

    def set_balance(self, balance_percent):
        self.current_tick_amp = balance_percent / 100.0
        self.current_noise_amp = (100 - balance_percent) / 100.0

    def _scheduler(self):
        now = time.time()
        next_tick = math.ceil(now / self.interval) * self.interval
        while not self.stop_event.is_set():
            sleep_time = next_tick - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            if self.stop_event.is_set():
                break
            self.tick_requested = True
            next_tick += self.interval
            if next_tick < time.time():
                next_tick = time.time() + self.interval

    def _audio_callback(self, outdata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)

        if self.tick_requested and not self.tick_playing:
            self.tick_playing = True
            self.tick_offset = 0
            self.tick_requested = False

        outdata[:] = 0.0
        for i in range(frames):
            # White noise
            noise_sample = random.uniform(-1.0, 1.0)

            tick_sample = 0.0
            if self.tick_playing:
                if self.tick_offset < self.tick_samples:
                    tick_sample = self.tick_wave[self.tick_offset]
                    self.tick_offset += 1
                else:
                    self.tick_playing = False

            sample = self.current_noise_amp * noise_sample + self.current_tick_amp * tick_sample
            outdata[i] = sample

    def start(self):
        self.stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self._audio_callback
        )
        self.stream.start()
        self.scheduler_thread = threading.Thread(target=self._scheduler, daemon=True)
        self.scheduler_thread.start()
        self.stop_event.clear()

    def stop(self):
        self.stop_event.set()
        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=1)

# ------------------------------------------------------------
# History storage
# ------------------------------------------------------------
HISTORY_FILE = "focus_mini_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def add_session(balance_percent):
    history = load_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "balance": balance_percent / 100.0
    })
    save_history(history)

def delete_session(index):
    history = load_history()
    if 0 <= index < len(history):
        del history[index]
        save_history(history)

def get_recommendation():
    history = load_history()
    if not history:
        return None
    avg = sum(item["balance"] for item in history) / len(history)
    return avg

# ------------------------------------------------------------
# Flet GUI
# ------------------------------------------------------------
def main(page: ft.Page):
    page.title = "Focus Mini"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20

    # Fixed window size
    page.window.width = 550
    page.window.height = 550
    page.window.resizable = False
    page.window.maximizable = False
    page.window.min_width = 550
    page.window.min_height = 550
    page.window.max_width = 550
    page.window.max_height = 550

    ACCENT_BLUE = ft.Colors.BLUE_400

    # Discrete slider (5% steps)
    balance_slider = ft.Slider(
        min=0, max=100, divisions=20, value=100,
        active_color=ACCENT_BLUE,
        thumb_color=ACCENT_BLUE,
        expand=True
    )
    slider_row = ft.Row([
        ft.Text("White Noise", size=14, weight=ft.FontWeight.W_500),
        balance_slider,
        ft.Text("Tick (Δt=5s)", size=14, weight=ft.FontWeight.W_500)
    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    # Button styles with default mouse cursor (no hand)
    start_button_style = ft.ButtonStyle(
        bgcolor=ACCENT_BLUE,
        color=ft.Colors.WHITE,
        padding=ft.Padding(24, 14, 24, 14),
        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
        mouse_cursor=ft.MouseCursor.BASIC
    )
    stop_button_style = ft.ButtonStyle(
        bgcolor=ft.Colors.RED_500,
        color=ft.Colors.WHITE,
        padding=ft.Padding(24, 14, 24, 14),
        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
        mouse_cursor=ft.MouseCursor.BASIC
    )

    start_btn = ft.Button("Start", icon="play_arrow", style=start_button_style)
    stop_btn = ft.Button("Stop", icon="stop", style=stop_button_style, visible=False)
    status_text = ft.Text("Ready", size=14)

    # Footer: made with DeepSeek + GitHub link below
    footer = ft.Column(
        [
            ft.Text("Made with help of DeepSeek", size=12, color=ft.Colors.GREY_500),
            ft.TextButton(
                "GitHub",
                url="https://github.com/hekawsh/focusmini",
                style=ft.ButtonStyle(
                    color=ft.Colors.GREY_500,
                    padding=0,
                    mouse_cursor=ft.MouseCursor.BASIC
                ),
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5
    )

    # Player container
    player_container = ft.Column([
        ft.Row([ft.Icon(ft.Icons.TIMER, size=40, color=ACCENT_BLUE),
                ft.Text("Focus Mini", size=32, weight=ft.FontWeight.BOLD, color=ACCENT_BLUE)],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20),
        slider_row,
        ft.Divider(height=25),
        ft.Row([start_btn, stop_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=10),
        ft.Row([footer], alignment=ft.MainAxisAlignment.CENTER),
    ], spacing=10)

    # History UI (scrollable)
    history_list = ft.ListView(expand=True, spacing=10)
    recommendation_text = ft.Text("", size=14)
    history_container = ft.Column([
        recommendation_text,
        ft.Container(content=history_list, height=350)
    ], spacing=20)

    # Navigation
    def show_player(e):
        player_container.visible = True
        history_container.visible = False
        player_nav_btn.style.bgcolor = ACCENT_BLUE
        history_nav_btn.style.bgcolor = ft.Colors.GREY_400
        page.update()

    def show_history(e):
        refresh_history_display()
        player_container.visible = False
        history_container.visible = True
        player_nav_btn.style.bgcolor = ft.Colors.GREY_400
        history_nav_btn.style.bgcolor = ACCENT_BLUE
        page.update()

    player_nav_btn = ft.Button("Player", on_click=show_player, style=ft.ButtonStyle(bgcolor=ACCENT_BLUE, color=ft.Colors.WHITE))
    history_nav_btn = ft.Button("History", on_click=show_history, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_400, color=ft.Colors.BLACK))
    nav_row = ft.Row([player_nav_btn, history_nav_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    def refresh_history_display():
        history = load_history()
        history_list.controls.clear()
        if not history:
            history_list.controls.append(ft.Text("No sessions recorded yet."))
        else:
            for idx, entry in enumerate(reversed(history)):
                dt = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
                bal = entry["balance"]
                tick_percent = int(bal * 100)
                noise_percent = 100 - tick_percent
                row = ft.Row([
                    ft.Text(f"{dt} → Tick: {tick_percent}% / White Noise: {noise_percent}%", expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_size=18,
                        on_click=lambda e, idx=idx: delete_entry(idx),
                        mouse_cursor=ft.MouseCursor.BASIC
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                history_list.controls.append(row)
        rec = get_recommendation()
        if rec is not None:
            rec_tick = int(rec * 100)
            rec_noise = 100 - rec_tick
            recommendation_text.value = f"Recommended balance: Tick {rec_tick}% / White Noise {rec_noise}%"
        else:
            recommendation_text.value = "No data yet. Start and stop a session to get recommendations."
        page.update()

    def delete_entry(reversed_idx):
        history = load_history()
        original_idx = len(history) - 1 - reversed_idx
        delete_session(original_idx)
        refresh_history_display()

    # App state
    is_running = False
    focus_session = None

    def update_balance(e):
        if is_running and focus_session:
            focus_session.set_balance(int(balance_slider.value))
        page.update()

    balance_slider.on_change = update_balance

    def start_focus(e):
        nonlocal is_running, focus_session
        if is_running:
            return
        balance_val = int(balance_slider.value)
        focus_session = TickNoiseFocus(balance_val)
        focus_session.start()
        status_text.value = "Running"
        status_text.color = ft.Colors.GREEN_500
        start_btn.visible = False
        stop_btn.visible = True
        page.update()
        is_running = True

    def stop_focus(e):
        nonlocal is_running, focus_session
        if not is_running:
            return
        if focus_session:
            current_balance = int(balance_slider.value)
            add_session(current_balance)
            focus_session.stop()
            focus_session = None
        status_text.value = "Stopped"
        status_text.color = ft.Colors.RED_500
        start_btn.visible = True
        stop_btn.visible = False
        page.update()
        is_running = False

    start_btn.on_click = start_focus
    stop_btn.on_click = stop_focus

    # Spacebar toggle
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == " ":
            if is_running:
                stop_focus(None)
            else:
                start_focus(None)
    page.on_keyboard_event = on_keyboard

    # Layout
    page.add(
        nav_row,
        ft.Divider(height=10),
        player_container,
        history_container,
    )
    history_container.visible = False
    page.update()

ft.run(main)