import yaml
from rapidfuzz import fuzz
import sys
import os

# -------------------------
# 📁 RESOURCE PATH (for EXE support)
# -------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -------------------------
# 📦 LOAD CONFIG
# -------------------------
with open(resource_path("config.yaml"), "r") as f:
    config = yaml.safe_load(f)


# -------------------------
# 🧠 PARSER
# -------------------------
def parse_command(text):
    original_text = text
    text = text.lower().strip()

    TRIGGERS = ["system", "nyra", "jarvis"]

    # ❌ Ignore if no trigger word
    if not any(t in text for t in TRIGGERS):
        return None, text

    # 🔥 Remove trigger word
    for t in TRIGGERS:
        if t in text:
            text = text.replace(t, "").strip()
            break

    # -------------------------
    # 🧠 CLEAN USER LANGUAGE
    # -------------------------
    IGNORE_WORDS = ["activate", "start", "launch", "please"]

    for word in IGNORE_WORDS:
        text = text.replace(word, "")

    text = text.strip()

    # 🔥 normalize mode → state
    text = text.replace("mode", "state")

    # -------------------------
    # 🔥 CLOSE EVERYTHING (FUZZY)
    # -------------------------
    if fuzz.partial_ratio("close all", text) > 70 or \
       fuzz.partial_ratio("close everything", text) > 70:
        return "close_all", text

    # -------------------------
    # ❌ CLOSE APP
    # -------------------------
    if text.startswith("close "):
        return "close_app", text

    # -------------------------
    # 🔥 GG SHORTCUT
    # -------------------------
    if "gg" in text:
        return "mode", "gg"

    # -------------------------
    # 🔥 MODE DETECTION (FUZZY)
    # -------------------------
    for mode in config.get("modes", {}):
        if fuzz.partial_ratio(mode, text) > 70:
            return "mode", mode

    # -------------------------
    # 🔓 OPEN APP
    # -------------------------
    if text.startswith("open "):
        return "open_app", text

    # -------------------------
    # 🌐 WEBSITE
    # -------------------------
    if "search" in text or "go to" in text:
        return "open_website", text

    # -------------------------
    # 🛑 EXIT SYSTEM
    # -------------------------
    if "stop" in text or "exit" in text:
        return "exit", text

    return None, text