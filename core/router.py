import os
import webbrowser
import yaml
import time
import string
from utils.feedback import speak, beep
from utils.feedback import play_sound, set_volume, get_volume

# 🔥 GLOBAL STATE
shutdown_pending = False
last_command = None
last_time = 0

# load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# 🔥 CUSTOM APP PATHS
APP_PATHS = {
    "whatsapp": r"C:\Users\praveen yadav\AppData\Local\WhatsApp\WhatsApp.exe",
    "opera gx": r"C:\Users\praveen yadav\AppData\Local\Programs\Opera GX\opera.exe",
    "notion": r"C:\Users\praveen yadav\AppData\Local\Programs\Notion\Notion.exe",
    "after effects": r"C:\Program Files\Adobe\Adobe After Effects 2020\Support Files\AfterFX.exe"
}

# -------------------------
# 🧠 HELPERS
# -------------------------

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()


def extract_app_name(text):
    text = clean_text(text)
    for word in ["open", "launch", "start"]:
        text = text.replace(word, "")
    return text.strip()


def extract_close_app(text):
    text = clean_text(text)
    for word in ["close", "kill", "stop"]:
        text = text.replace(word, "")
    return text.strip()


# -------------------------
# ⚙️ MODE EXECUTION
# -------------------------

def run_mode(mode_name):
    mode = config["modes"].get(mode_name)

    print("MODE RECEIVED:", mode_name)
    print("AVAILABLE MODES:", config["modes"].keys())

    if not mode:
        speak("Mode not found")
        return

    # 🔥 GG / SOUND MODE (NO RESET)
    if "sound" in mode and not mode.get("apps"):
        old_vol = get_volume()

        set_volume(0.3)
        play_sound(mode["sound"])

        speak("Good game")

        time.sleep(3)
        set_volume(old_vol)

        return

    # 🔥 NORMAL MODES
    speak("Resetting system")

    ALL_APPS = [
        "opera.exe",
        "whatsapp.exe",
        "notepad.exe",
        "notion.exe",
        "AfterFX.exe",
        "discord.exe",
        "explorer.exe",
        "Code.exe"
    ]

    for app in ALL_APPS:
        os.system(f"taskkill /im {app} /f")

    time.sleep(2)

    # restore explorer
    os.system("start explorer.exe")
    time.sleep(1)

    speak(f"{mode_name} activated")

    # 🔥 OPEN APPS
    for app in mode.get("apps", []):
        try:
            if app in APP_PATHS:
                os.startfile(APP_PATHS[app])
            else:
                os.system(f"start {app}")
        except:
            speak(f"{app} not found")

        time.sleep(1)

    # 🌐 OPEN WEBSITES
    for site in mode.get("websites", []):
        webbrowser.open(site)
        time.sleep(1)

    # 🔊 OPTIONAL SOUND
    if "sound" in mode:
        play_sound(mode["sound"])

    speak("Environment ready")


# -------------------------
# 🚀 ROUTER
# -------------------------

def route_command(command, text):
    global shutdown_pending, last_command, last_time

    if command is None:
        return

    current_time = time.time()

    # 🔥 BLOCK DUPLICATES
    if command == last_command and (current_time - last_time) < 3:
        return

    last_command = command
    last_time = current_time

    beep()

    # 🔥 SHUTDOWN CONFIRMATION
    if shutdown_pending:
        if "confirm" in text:
            speak("Shutting down system")
            os.system("shutdown /s /t 3")
        elif "cancel" in text:
            speak("Shutdown cancelled")

        shutdown_pending = False
        return

    # 🔥 MODE
    if command == "mode":
        result = run_mode(text)

        if result == "awaiting_shutdown_confirmation":
            shutdown_pending = True
        return

    # 🛑 EXIT
    elif command == "exit":
        speak("Shutting down system")
        exit()

    # 🔓 OPEN APP
    elif command == "open_app":
        app_name = extract_app_name(text)

        if not app_name:
            speak("Say the app name")
            return

        speak(f"Opening {app_name}")

        if app_name in APP_PATHS:
            os.startfile(APP_PATHS[app_name])
        else:
            os.system(f"start {app_name}")

    # 🌐 WEBSITE
    elif command == "open_website":
        query = clean_text(text.replace("search", "").replace("go to", ""))
        speak("Opening website")
        webbrowser.open(f"https://{query}")

    # ❌ CLOSE APP
    elif command == "close_app":
        app = extract_close_app(text)

        if app in ["all", "everything", ""]:
            return

        mapping = {
            "notepad": "notepad.exe",
            "opera": "opera.exe",
            "notion": "notion.exe",
            "whatsapp": "whatsapp.exe",
            "after effects": "AfterFX.exe"
        }

        app = mapping.get(app, app + ".exe")

        speak(f"Closing {app}")
        os.system(f"taskkill /im {app} /f")

    # 🔥 CLOSE ALL
    elif command == "close_all":
        speak("Closing everything")

        apps = [
            "notepad.exe",
            "opera.exe",
            "whatsapp.exe",
            "notion.exe",
            "AfterFX.exe"
        ]

        for app in apps:
            os.system(f"taskkill /im {app} /f")