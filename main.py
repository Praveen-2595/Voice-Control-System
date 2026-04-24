import time
from core.listener import listen
from core.recognizer import recognize
from core.parser import parse_command
from core.router import route_command
from utils.logger import logger
from utils.feedback import beep

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

last_command = None
last_time = 0


def main():
    logger.info("Voice Control System Started 🎤")

    while True:
        audio = listen()
        if audio is None:
            continue

        text = recognize(audio)

        print(f"DEBUG TEXT: {text}")

        if "system" not in text:
            continue
        if not text:
            continue

        logger.info(f"You said: {text}")

        command, value = parse_command(text)

# 🔥 DO NOT EXECUTE IF NO COMMAND
        if command is None:
            continue
        if text:
            beep()   # 🔥 confirms voice detected
        route_command(command, value)
        print("COMMAND:", command)

        # after route_command(...)
        route_command(command, value)

        time.sleep(1.5)  # 🔥 cooldown
if __name__ == "__main__":
    main()