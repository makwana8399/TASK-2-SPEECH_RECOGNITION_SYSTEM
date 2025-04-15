import speech_recognition as sr
import datetime
import os

def create_filename():
    """Generate a timestamped filename."""
    now = datetime.datetime.now()
    return f"recording_{now.strftime('%Y%m%d_%H%M%S')}.wav"

def save_audio_to_file(audio, filename):
    """Save the recorded audio to a WAV file."""
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    print(f"✅ Audio saved to {filename}")

def recognize_speech_from_mic(recognizer, mic):
    """Capture speech from the mic and return text."""
    with mic as source:
        print("🎤 Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎙️ Start speaking!")
        audio = recognizer.listen(source)
        print("🔁 Processing...")

    return audio

def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎧 Speech-to-Text System (Press Ctrl+C to exit)\n")

    while True:
        try:
            audio = recognize_speech_from_mic(recognizer, mic)

            # Save audio file
            filename = create_filename()
            save_audio_to_file(audio, filename)

            # Recognize using Google Web Speech API
            print("🧠 Recognizing...")
            text = recognizer.recognize_google(audio)
            print("📝 Transcription:", text)

        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
        except sr.RequestError as e:
            print(f"🚨 API request error: {e}")
        except KeyboardInterrupt:
            print("\n👋 Exiting. Goodbye!")
            break
        except Exception as ex:
            print(f"⚠️ Unexpected error: {ex}")

if __name__ == "__main__":
    main()
