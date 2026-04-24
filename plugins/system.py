import os
from utils.feedback import speak

def open_notepad():
    speak("Opening Notepad")
    os.system("notepad")

def open_chrome():
    speak("Opening Chrome")
    os.system("start chrome")