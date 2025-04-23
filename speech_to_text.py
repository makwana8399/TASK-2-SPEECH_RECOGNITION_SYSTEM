import speech_recognition as sr
import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from tkinter import font

# Flag to control listening loop
is_listening = False

def create_filename():
    now = datetime.datetime.now()
    return f"recording_{now.strftime('%Y%m%d_%H%M%S')}.wav"

def save_audio_to_file(audio, filename):
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    print(f"✅ Audio saved to {filename}")

def recognize_speech_from_mic(recognizer, mic):
    with mic as source:
        print("🎤 Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎙️ Start speaking!")
        audio = recognizer.listen(source)
        print("🔁 Processing...")
    return audio

def start_recognition():
    """Start the speech recognition process in a separate thread."""
    global is_listening
    is_listening = True

    def recognition_thread():
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        while is_listening:
            try:
                audio = recognize_speech_from_mic(recognizer, mic)
                filename = create_filename()
                save_audio_to_file(audio, filename)

                result = recognizer.recognize_google(audio)
                text_output.delete(1.0, tk.END)
                text_output.insert(tk.END, result)
                print("📝 Transcription:", result)

            except sr.UnknownValueError:
                print("❌ Could not understand the audio.")
            except sr.RequestError as e:
                print(f"🚨 API request error: {e}")
            except Exception as ex:
                print(f"⚠️ Unexpected error: {ex}")

    Thread(target=recognition_thread, daemon=True).start()

def stop_recognition():
    """Stop the speech recognition process."""
    global is_listening
    is_listening = False
    print("🛑 Stopped listening.")

def save_audio_clip():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    try:
        audio = recognize_speech_from_mic(recognizer, mic)
        filename = create_filename()
        folder_selected = filedialog.askdirectory(title="Select Folder to Save Audio Clip")
        if folder_selected:
            full_path = os.path.join(folder_selected, filename)
            save_audio_to_file(audio, full_path)
            messagebox.showinfo("Success", f"Audio saved to {full_path}")
        else:
            messagebox.showwarning("No Folder Selected", "No folder selected, audio not saved.")
    except Exception as ex:
        messagebox.showerror("Error", f"An error occurred: {ex}")

# Create the main GUI window
root = tk.Tk()
root.title("🎤 SPEECH RECOGNITION SYSTEM 🤖")
root.geometry("500x450")

bold_font = font.Font(weight="bold", size=10)

# GUI Components
start_button = tk.Button(root, text="Start Recognition", command=start_recognition, width=20, height=2)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Listening", command=stop_recognition, width=20, height=2)
stop_button.pack(pady=10)

save_button = tk.Button(root, text="Save Audio Clip", command=save_audio_clip, width=20, height=2)
save_button.pack(pady=10)

output_label = tk.Label(root, text="📝 Transcription Output:", font=("Helvetica", 10, "bold"))
output_label.pack(pady=(20, 5))

text_output = tk.Text(root, height=10, width=50, font=bold_font)
text_output.pack(pady=5)

# Run the GUI loop
root.mainloop()