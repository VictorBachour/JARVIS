import speech_recognition as sr
import pyttsx3
import os
import time

class Jarvis:
    def __init__(self):
        self.wake_word = "jarvis"
        self.recognizer = sr.Recognizer()
        self.wake_word_said = False

    def open_app(self):
        print("In open app")

    def main_loop(self):
        with sr.Microphone() as source:
            text = None
            while(self.wake_word_said is False):
                try:
                    self.recognizer.adjust_for_ambient_noise(source)
                    word = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(word).lower()
                    if(self.wake_word in text):
                        self.wake_word_said = True
                except sr.UnknownValueError:
                    None
            self.open_app()



jarvis = Jarvis()
jarvis.main_loop()
