import speech_recognition as sr
import pyttsx3
import os
import shutil
import subprocess


class Jarvis:
    def __init__(self):
        self.wake_word = "jarvis"
        self.recognizer = sr.Recognizer()
        self.wake_word_said = False
        self.open_was_said = False
        self.close_was_said = False

    def _speak(self, message):
        narrator = pyttsx3.init()

        narrator.setProperty('rate', 150)
        narrator.setProperty('volume', 1)

        narrator.say(message)
        narrator.runAndWait()

    def splitting_text(self, text_to_split):
        keyword = 'open' if self.open_was_said else 'close'
        words = text_to_split.split()
        try:
            keyword_index = words.index(keyword)
            app_name = " ".join(words[keyword_index + 1:]).strip()
            if app_name:
                return app_name
            else:
                self._speak(f"No application specified after '{keyword}'.")
        except ValueError:
            self._speak(f"Keyword '{keyword}' not found in the command.")
        return None
#prompt the user to input where his apps are and to paste the directory in command prompt this will only be done once
#to make it done once check to see if the notepad is empty if empty prompt user if not move on to main_loop
    def open_app(self, app_to_open):
        None

    def close_app(self, app_to_close):
        if app_to_close:
            print(f"Closing: {app_to_close}")
            self._speak(f"Closing {app_to_close}")
            # Add your logic to close the app here (e.g., os.system())
        else:
            self._speak("No application name provided to close.")

    def open_or_close_app(self):
        self._speak("What would you like me to open or close? Please say one command at a time. or if you did not mean "
                    "to call just say stop.")
        still_listening = True
        with sr.Microphone() as source:
            while still_listening:
                try:
                    self.recognizer.adjust_for_ambient_noise(source)
                    word = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(word).lower()

                    if 'open' in text:
                        self.open_was_said = True
                        app_name = self.splitting_text(text)
                        self.open_app(app_name)
                        break
                    elif 'close' in text:
                        self.close_was_said = True
                        app_name = self.splitting_text(text)
                        self.close_app(app_name)
                        break
                    elif text == "stop":
                        still_listening = False
                    else:
                        self._speak("I didn't catch a valid command. Please say 'open' or 'close'.")
                except sr.UnknownValueError:
                    self._speak("Sorry, I didn't understand. Could you repeat that?")
        self.main_loop()

    def main_loop(self):
        self._speak("Hello, just speak my name and I will be able to assist you.")
        with sr.Microphone() as source:
            while not self.wake_word_said:
                try:
                    self.recognizer.adjust_for_ambient_noise(source)
                    word = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(word).lower()
                    print(f"User said: {text}")

                    if self.wake_word in text:
                        self.wake_word_said = True
                        self._speak("Yes, I'm here. How can I assist?")
                        self.open_or_close_app()
                except sr.UnknownValueError:
                    print("Listening for wake word...")
jarvis = Jarvis()
jarvis.main_loop()