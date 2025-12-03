#!/usr/bin/env python3
"""
Press-to-talk dictation using Whisper.
Hold Right Ctrl to record, release to transcribe.
"""
import sounddevice as sd
import numpy as np
import whisper
import subprocess
import threading
from pynput import keyboard

SAMPLE_RATE = 16000
HOTKEY = keyboard.Key.ctrl_r  # Right Ctrl key

# State
recording = False
audio_chunks = []
model = None
target_window = None

def load_model():
    global model
    print("Loading Whisper model...", flush=True)
    model = whisper.load_model("small")
    device = next(model.parameters()).device
    print(f"Model loaded on {device.type.upper()}.", flush=True)
    print("Hold Right Ctrl to speak, release to transcribe.", flush=True)
    print("Press Ctrl+C to exit.\n", flush=True)

def start_recording():
    global recording, audio_chunks, target_window
    if recording:
        return
    # Save the currently focused window before we start
    try:
        result = subprocess.run(["xdotool", "getactivewindow"], capture_output=True, text=True)
        target_window = result.stdout.strip()
    except:
        target_window = None
    recording = True
    audio_chunks = []
    print("🎤 Recording...", end="", flush=True)

    def callback(indata, frames, time, status):
        if recording:
            audio_chunks.append(indata.copy())

    global stream
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=callback
    )
    stream.start()

def stop_recording():
    global recording, stream
    if not recording:
        return
    recording = False
    stream.stop()
    stream.close()
    print(" stopped", flush=True)
    print("=" * 50, flush=True)

    if not audio_chunks:
        print("No audio recorded.")
        print("=" * 50 + "\n", flush=True)
        return

    audio = np.concatenate(audio_chunks).flatten()
    transcribe(audio)

def transcribe(audio):
    print("Transcribing...", end="", flush=True)
    result = model.transcribe(audio, fp16=True)
    text = result["text"].strip()
    print(" done", flush=True)

    if text:
        print(f"\n📝 TRANSCRIPTION:\n", flush=True)
        print(f"    {text}\n", flush=True)
        copy_to_clipboard(text)
        type_to_terminal(text)
    else:
        print("\n⚠️  No speech detected.", flush=True)

    print("=" * 50, flush=True)
    print("Ready. Hold Right Ctrl to speak.\n", flush=True)

def copy_to_clipboard(text):
    try:
        subprocess.run(["xclip", "-selection", "clipboard"],
                      input=text.encode(), check=True)
        print("(copied to clipboard)", flush=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # xclip not available

def type_to_terminal(text):
    """Type text into the previously active window using xdotool."""
    global target_window
    try:
        if target_window:
            # Focus the original window and type into it
            subprocess.run(["xdotool", "windowactivate", "--sync", target_window], check=True)
            subprocess.run(["xdotool", "type", "--clearmodifiers", "--", text], check=True)
            print("(typed to terminal)", flush=True)
        else:
            print("(no target window saved)", flush=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"(xdotool error: {e})", flush=True)

def on_press(key):
    if key == HOTKEY:
        start_recording()

def on_release(key):
    if key == HOTKEY:
        threading.Thread(target=stop_recording, daemon=True).start()

def main():
    load_model()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    main()
