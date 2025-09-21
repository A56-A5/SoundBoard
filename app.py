import asyncio
import edge_tts
import tkinter as tk
from tkinter import messagebox
import pygame
import speech_recognition as sr
import threading
import queue
import tempfile
import os

STOP_PHRASE = "stop recording"

# --- TTS Queue & Worker ---
tts_queue = queue.Queue()

def tts_worker():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    while True:
        text = tts_queue.get()
        if text is None:
            break
        loop.run_until_complete(generate_tts(text))
        tts_queue.task_done()

# --- Get Settings ---
def get_tts_settings():
    voice = voice_var.get()
    
    # Voice rate (speed)
    rate_val = rate_var.get()
    rate = f"{'+' if rate_val >= 0 else ''}{rate_val}%"

    # Volume
    vol_val = volume_var.get()
    volume = f"{'+' if vol_val >= 0 else ''}{vol_val}%"

    return voice, rate, volume

# --- TTS Generation ---
async def generate_tts(text):
    if not text.strip():
        return
    try:
        # Stop any current playback
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        voice, rate, volume = get_tts_settings()

        # Create a unique temp file for each TTS request
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_file = tmp.name

        communicate = edge_tts.Communicate(
            text,
            voice=voice,
            rate=rate,
            volume=volume
        )
        await communicate.save(tmp_file)

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(tmp_file)
        pygame.mixer.music.set_volume(volume_var.get() / 100)  # FIXED: apply slider
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        # Safe deletion
        try:
            os.remove(tmp_file)
        except PermissionError:
            pass

    except Exception as e:
        messagebox.showerror("Error", f"TTS failed:\n{e}")

# --- Playback Controls ---
def pause_audio():
    if pygame.mixer.get_init():
        pygame.mixer.music.pause()

def resume_audio():
    if pygame.mixer.get_init():
        pygame.mixer.music.unpause()

def stop_audio():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

# --- Speak Button Handler ---
def speak_text():
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        tts_queue.put(text)
    else:
        messagebox.showinfo("Info", "Please type something first!")

# --- Background Mic Listener ---
def listen_in_background():
    recognizer = sr.Recognizer()
    collected_text = []

    def run_listener():
        with sr.Microphone() as source:
            status_label.config(text=f"🎤 Listening... say '{STOP_PHRASE}' to finish", fg="#00ffcc")
            while True:
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                    try:
                        spoken = recognizer.recognize_google(audio).lower()
                        if STOP_PHRASE in spoken:
                            status_label.config(text=f"✅ Done (detected '{STOP_PHRASE}')", fg="#00ff00")
                            break
                        collected_text.append(spoken)
                        text_entry.delete("1.0", tk.END)
                        text_entry.insert(tk.END, " ".join(collected_text))
                        tts_queue.put(spoken)
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        messagebox.showerror("Mic Error", f"API error:\n{e}")
                        break
                except Exception as e:
                    messagebox.showerror("Mic Error", f"Something went wrong:\n{e}")
                    status_label.config(text="⚠️ Error", fg="#ff0066")
                    break

    threading.Thread(target=run_listener, daemon=True).start()

# --- Tkinter UI ---
root = tk.Tk()
root.title("Realtime Dictation + TTS")
root.geometry("700x620")
root.configure(bg="#1a1a1a")
root.resizable(False, False)

fg_color = "#00ffcc"
bg_color = "#1a1a1a"
font_style = ("Press Start 2P", 10)

title = tk.Label(root, text="Realtime Dictation + TTS", font=font_style, fg=fg_color, bg=bg_color)
title.pack(pady=10)

text_entry = tk.Text(root, height=6, width=75, font=font_style, fg=fg_color,
                     bg="#000000", insertbackground=fg_color, relief="solid", borderwidth=3)
text_entry.pack(pady=5)

mic_button = tk.Button(root, text=f"🎤 SPEAK (say '{STOP_PHRASE}')", font=font_style,
                       fg="#ffffff", bg="#3333ff", activebackground="#6666ff",
                       activeforeground="white", relief="flat", command=listen_in_background)
mic_button.pack(pady=10)

speak_button = tk.Button(root, text="🗣️ SPEAK TEXT", font=font_style,
                         fg="white", bg="#ff6600", activebackground="#ff9933",
                         activeforeground="white", relief="flat", command=speak_text)
speak_button.pack(pady=5)

# Playback control buttons
controls_frame = tk.Frame(root, bg=bg_color)
controls_frame.pack(pady=10)

pause_btn = tk.Button(controls_frame, text="⏸️ PAUSE", font=font_style,
                      fg="white", bg="#5555ff", command=pause_audio)
pause_btn.grid(row=0, column=0, padx=5)

resume_btn = tk.Button(controls_frame, text="▶️ RESUME", font=font_style,
                       fg="white", bg="#22aa22", command=resume_audio)
resume_btn.grid(row=0, column=1, padx=5)

stop_btn = tk.Button(controls_frame, text="⏹️ STOP", font=font_style,
                     fg="white", bg="#aa2222", command=stop_audio)
stop_btn.grid(row=0, column=2, padx=5)

status_label = tk.Label(root, text="Idle...", font=font_style, fg="#888888", bg=bg_color)
status_label.pack(pady=5)

# --- Settings Panel ---
settings_title = tk.Label(root, text="⚙️ SETTINGS", font=font_style, fg="#ffcc00", bg=bg_color)
settings_title.pack(pady=5)

settings_frame = tk.Frame(root, bg=bg_color)
settings_frame.pack(pady=5)

# Voices
voice_var = tk.StringVar(value="en-US-GuyNeural")
voices = [
    "en-US-GuyNeural",
    "en-US-JennyNeural",
    "en-GB-RyanNeural",
    "en-GB-SoniaNeural",
    "en-IN-PrabhatNeural",
    "en-IN-NeerjaNeural",
]
voice_label = tk.Label(settings_frame, text="Voice:", font=font_style, fg=fg_color, bg=bg_color)
voice_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
voice_menu = tk.OptionMenu(settings_frame, voice_var, *voices)
voice_menu.config(font=font_style, bg="#000000", fg=fg_color, activebackground="#333333", activeforeground=fg_color)
voice_menu["menu"].config(bg="#000000", fg=fg_color)
voice_menu.grid(row=0, column=1, padx=5, pady=5)

# Rate (speed)
rate_var = tk.IntVar(value=0)
rate_label = tk.Label(settings_frame, text="Speed:", font=font_style, fg=fg_color, bg=bg_color)
rate_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
rate_slider = tk.Scale(settings_frame, variable=rate_var, from_=-50, to=50,
                       orient="horizontal", bg=bg_color, fg=fg_color,
                       troughcolor="#000000", highlightthickness=0, length=250)
rate_slider.grid(row=1, column=1, padx=5, pady=5)

# Volume
volume_var = tk.IntVar(value=100)
volume_label = tk.Label(settings_frame, text="Volume:", font=font_style, fg=fg_color, bg=bg_color)
volume_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
volume_slider = tk.Scale(settings_frame, variable=volume_var, from_=0, to=200,
                         orient="horizontal", bg=bg_color, fg=fg_color,
                         troughcolor="#000000", highlightthickness=0, length=250)
volume_slider.grid(row=2, column=1, padx=5, pady=5)

footer = tk.Label(root, text="Python + edge-tts + SpeechRecognition", font=("Press Start 2P", 7),
                  fg="#555555", bg=bg_color)
footer.pack(side="bottom", pady=5)

# --- Start Worker ---
threading.Thread(target=tts_worker, daemon=True).start()

root.mainloop()
tts_queue.put(None)
