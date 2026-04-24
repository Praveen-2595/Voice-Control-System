import pyttsx3
import winsound
import threading
import sys
import os

# -------------------------
# 🗣️ TEXT TO SPEECH
# -------------------------

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

def speak(text):
    print("🗣️", text)
    engine.say(text)
    engine.runAndWait()


# -------------------------
# 🔔 BEEP SIGNAL
# -------------------------

def beep():
    try:
        winsound.Beep(1000, 150)
    except:
        pass


# -------------------------
# 📁 RESOURCE PATH (for EXE later)
# -------------------------

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# -------------------------
# 🎵 PLAY SOUND (BACKGROUND)
# -------------------------

import subprocess

current_process = None

def play_sound(file):
    global current_process

    try:
        # 🔥 stop previous sound
        if current_process:
            current_process.kill()

        path = resource_path(file)

        # 🔥 play using Windows native player
        current_process = subprocess.Popen(
            ["powershell", "-c", f'(New-Object Media.SoundPlayer "{path}").PlaySync();']
        )

    except Exception as e:
        print("Sound error:", e)

# -------------------------
# 🔊 VOLUME CONTROL (SAFE VERSION)
# -------------------------

# Try pycaw first
try:
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    def get_volume():
        try:
            speakers = AudioUtilities.GetSpeakers()
            interface = speakers.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            return volume.GetMasterVolumeLevelScalar()
        except:
            return 0.5  # fallback

    def set_volume(level):
        try:
            speakers = AudioUtilities.GetSpeakers()
            interface = speakers.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level, None)
        except:
            pass

except:
    # 🔥 FALLBACK METHOD (ALWAYS WORKS)
    import pyautogui

    def set_volume(level):
        try:
            # reset volume
            for _ in range(50):
                pyautogui.press("volumedown")

            # set approx level
            steps = int(level * 50)
            for _ in range(steps):
                pyautogui.press("volumeup")
        except:
            pass

    def get_volume():
        return 0.5  # dummy fallback