import sounddevice as sd
import queue
import numpy as np
from pynput import keyboard

q = queue.Queue()
recording = False

def callback(indata, frames, time, status):
    if recording:
        q.put(indata.copy())

def listen():
    global recording

    audio_data = []

    def on_press(key):
        global recording
        if key == keyboard.Key.space:
            if not recording:
                print("🎤 Recording...")
                recording = True

    def on_release(key):
        global recording
        if key == keyboard.Key.space:
            recording = False
            return False  # stop listener

    print("🟢 Hold SPACE to speak...")

    # wait until SPACE pressed + released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        with sd.InputStream(
            samplerate=16000,
            blocksize=8000,
            dtype='int16',
            channels=1,
            callback=callback,
            device=2
        ):
            listener.join()

    if not recording and not q.empty():
        while not q.empty():
            data = q.get()
            audio_data.append(data)

            volume = int(np.abs(data).mean())
            print("Volume:", volume)

    if not audio_data:
        return None

    audio_data = np.concatenate(audio_data, axis=0)
    return audio_data.tobytes()