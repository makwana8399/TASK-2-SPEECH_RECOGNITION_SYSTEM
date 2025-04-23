import tkinter as tk
from tkinter import filedialog, messagebox, font
import speech_recognition as sr
from pydub import AudioSegment
import os

# Transcribe selected audio file
def transcribe_audio():
    recognizer = sr.Recognizer()
    file_path = filedialog.askopenfilename(
        title="Select an Audio File",
        filetypes=[("Audio Files", "*.wav *.flac *.mp3")]
    )

    if not file_path:
        messagebox.showinfo("Cancelled", "No file selected.")
        return

    try:
        status_label.config(text="🔄 Processing...")

        # Convert mp3 to wav if necessary
        if file_path.lower().endswith("task2audioclip.mp3.mp3"):
            audio_mp3 = AudioSegment.from_mp3(file_path)
            temp_wav_path = "temp_audio.wav"
            audio_mp3.export(temp_wav_path, format="wav")
            file_path_to_use = temp_wav_path
        else:
            file_path_to_use = file_path

        with sr.AudioFile(file_path_to_use) as source:
            audio = recognizer.record(source)

        result = recognizer.recognize_google(audio)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, result)
        status_label.config(text="Transcription Complete ✅")

        # Clean up temporary file if created
        if file_path.lower().endswith(".mp3") and os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

    except sr.UnknownValueError:
        status_label.config(text="❌ Could not understand audio.")
    except sr.RequestError as e:
        status_label.config(text=f"🚨 API Error: {e}")
    except Exception as ex:
        status_label.config(text=f"⚠️ Error: {ex}")

# Clear transcribed text
def clear_text():
    text_output.delete(1.0, tk.END)
    status_label.config(text="Text cleared🧹")

# GUI setup
root = tk.Tk()
root.title("Speech Recognition System 🎧")
root.geometry("650x550")
root.configure(bg="black")  # Set background color

bold_font = font.Font(weight="bold", size=10)

title_label = tk.Label(root, text="Import Audio Clip to Transcribe", font=("Unbounded", 14, "bold"),
                       bg="black", fg="white")
title_label.pack(pady=15)

import_button = tk.Button(root, text="Import Audio", command=transcribe_audio, width=25, height=2,
                          bg="gray20", fg="white", activebackground="gray30")
import_button.pack(pady=10)

output_label = tk.Label(root, text="Transcribed Text :", font=("Poppins", 10, "bold"),
                        bg="black", fg="white")
output_label.pack(pady=(20, 5))

text_output = tk.Text(root, height=10, width=50, font=bold_font,
                      bg="gray15", fg="white", insertbackground="white")
text_output.pack(pady=5)

clear_button = tk.Button(root, text="Clear Text", command=clear_text, width=15, height=1,
                         bg="gray20", fg="white", activebackground="gray30")
clear_button.pack(pady=(5, 10))

status_label = tk.Label(root, text="", font=("Poppins", 10, "italic"), fg="lightgreen", bg="black")
status_label.pack(pady=5)

root.mainloop()