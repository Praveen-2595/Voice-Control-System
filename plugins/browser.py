import webbrowser
from utils.feedback import speak

def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")