import asyncio
import edge_tts
import tkinter as tk
from tkinter import messagebox
import pygame
import speech_recognition as sr
import threading

OUTPUT_FILE = "output.mp3"
STOP_PHRASE = "stop recording"

# --- TTS Generation ---
async def generate_tts(text, voice="en-US-GuyNeural"):
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(OUTPUT_FILE)

        pygame.mixer.init()
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", f"TTS failed:\n{e}")

# --- Speak Button Handler ---
def speak_text():
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        asyncio.run(generate_tts(text))
    else:
        messagebox.showinfo("Info", "Please type something first!")

# --- Background Mic Listener (Live Updates) ---
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
                        collected_text.append(spoken)

                        # Update UI live
                        text_entry.delete("1.0", tk.END)
                        text_entry.insert(tk.END, " ".join(collected_text))

                        if STOP_PHRASE in spoken:
                            status_label.config(text=f"✅ Done (detected '{STOP_PHRASE}')", fg="#00ff00")
                            break
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        messagebox.showerror("Mic Error", f"API error:\n{e}")
                        break
                except Exception as e:
                    messagebox.showerror("Mic Error", f"Something went wrong:\n{e}")
                    status_label.config(text="⚠️ Error", fg="#ff0066")
                    break

        # Remove stop phrase from final text
        final_text = " ".join(collected_text).replace(STOP_PHRASE, "").strip()
        text_entry.delete("1.0", tk.END)
        text_entry.insert(tk.END, final_text)

        # Run TTS once
        if final_text:
            asyncio.run(generate_tts(final_text))

    threading.Thread(target=run_listener, daemon=True).start()

# --- Tkinter UI ---
root = tk.Tk()
root.title("TTS")
root.geometry("580x400")
root.configure(bg="#1a1a1a")
root.resizable(False, False)

fg_color = "#00ffcc"
bg_color = "#1a1a1a"
font_style = ("Press Start 2P", 10)

title = tk.Label(root, text="TTS", font=font_style, fg=fg_color, bg=bg_color)
title.pack(pady=10)

text_entry = tk.Text(root, height=6, width=55, font=font_style, fg=fg_color,
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

status_label = tk.Label(root, text="Idle...", font=font_style, fg="#888888", bg=bg_color)
status_label.pack(pady=5)

footer = tk.Label(root, text="Python + edge-tts + SpeechRecognition", font=("Press Start 2P", 7),
                  fg="#555555", bg=bg_color)
footer.pack(side="bottom", pady=5)

root.mainloop()
