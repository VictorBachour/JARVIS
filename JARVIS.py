import speech_recognition as sr
import pyttsx3
import os
import time

class Jarvis:
    def __init__(self):
        self.wake_word = "Jarvis"
        self.recognizer = sr.Recognizer()
        self.wake_word_said = False

    def open_app(self):
        print("Listening for words")
    def main_loop(self):
        while self.wake_word_said is False:
            # just trying to get microphone ot work then should check to see if jarvis is said in here
            # then should call listen to see what user wants


jarvis = Jarvis()
jarvis.main_loop()
