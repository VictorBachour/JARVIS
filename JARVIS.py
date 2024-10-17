import speech_recognition as sr
import pyttsx3
import os
import time

class Jarvis:
    def __init__(self):
        self.wake_word = "jarvis"
        self.recognizer = sr.Recognizer()
        self.wake_word_said = False
        self.what_to_do_with_app = None
        self.open_was_said = False
        self.close_was_said = False
#work on open or close first find if there is maybe a narrator
#then work on opening app with narrator what would you like me to do?
#then close based on what i know with opening
    def open_app(self):
        print("In open app")
    def close_app(self):
        print('In close app')
    def open_or_close_app(self):
        print('in open or close app')
    def main_loop(self):
        with sr.Microphone() as source:
            text = None
            while(self.wake_word_said is False):
                try:
                    print('getting rid of ambience')
                    self.recognizer.adjust_for_ambient_noise(source)
                    print('listening')
                    word = self.recognizer.listen(source)
                    print('translating')
                    text = self.recognizer.recognize_google(word).lower()
                    print(f'the text that was said is {text}')
                    if('open' in text and 'close' in text):
                        None
                    elif(self.wake_word in text):
                        self.wake_word_said = True
                    if('open' in text and self.wake_word_said):
                        self.open_was_said = True
                    if('close' in text and self.wake_word_said):
                        self.close_was_said = True
                    if(self.close_was_said is False and self.open_was_said is False and self.wake_word_said is True):
                        self.open_or_close_app()
                except sr.UnknownValueError:
                    None
            self.open_app() if self.open_was_said else None
            self.close_app() if self.close_was_said else None




jarvis = Jarvis()
jarvis.main_loop()
