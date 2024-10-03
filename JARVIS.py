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
        print("Listening for words")

    def main_loop(self):
        while self.wake_word_said is False:
            with sr.Microphone() as source:
                print('getting rid of ambient au')
                self.recognizer.adjust_for_ambient_noise(source)
                text = None
                try:
                    print("listening")
                    while(text == None or text.contains(self.wake_word) == False):
                        word = self.recognizer.listen(source)
                        text = self.recognizer.recognize_google(word).lower()
                    self.wake_word = True
                except sr.UnknownValueError:
                    print("Sorry, I could not understand the audio.")
                except sr.RequestError:
                    print("Sorry, there was an issue with the speech recognition service.")
            #get it to just always listen for words then always just add then delete words maybe?

jarvis = Jarvis()
jarvis.main_loop()
