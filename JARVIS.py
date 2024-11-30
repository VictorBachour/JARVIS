import speech_recognition as sr
import pyttsx3
import os
import subprocess
import psutil

class Jarvis:
    def __init__(self):
        self.wake_word = "jarvis"
        self.recognizer = sr.Recognizer()
        self.open_was_said = False
        self.close_was_said = False
        self.apps_file = "folder_that_leads_to_apps.txt"

        if os.path.exists(self.apps_file):
            with open(self.apps_file, 'r') as f:
                folder_path = f.read().strip()

            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                self.open_app('Spotify')
            else:
                self._speak("Saved folder path is invalid or does not exist.")
                self.prompt_user_for_apps_folder()
        else:
            self._speak("Apps file not found. Prompting user for apps folder.")
            self.prompt_user_for_apps_folder()

    def _speak(self, message):
        narrator = pyttsx3.init()

        narrator.setProperty('rate', 190)
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

    # prompt the user to input where his apps are and to paste the directory in command prompt this will only be done
    # once to make it done once check to see if the notepad is empty if empty prompt user if not move on to main_loop
    def open_app(self, app_to_open):

        if not app_to_open:
            self._speak("No application name provided to open.")
            return

        if os.path.exists(self.apps_file):
            with open(self.apps_file, 'r') as f:
                folder_path = f.read().strip()

        if folder_path and os.path.isdir(folder_path):
            app_path = os.path.join(folder_path, app_to_open)
            if not os.path.exists(app_path):
                app_path = os.path.join(folder_path, app_to_open + ".lnk")
            if not os.path.exists(app_path):
                app_path = os.path.join(folder_path, app_to_open + ".exe")
            if not os.path.exists(app_path):
                app_path = os.path.join(folder_path, app_to_open + ".url")
            if os.path.exists(app_path):
                try:
                    app_path = f'"{app_path}"'
                    subprocess.run(app_path, check=True, shell=True)
                    self._speak(f"Currently opening {app_to_open}.")
                except Exception as e:
                    self._speak(f"Failed to open {app_to_open}. Error: {str(e)}")
                else:
                    self._speak(f"{app_to_open} does not exist in the specified folder.")
            else:
                self._speak("Apps folder path is invalid or not set.")
                self.prompt_user_for_apps_folder()
        else:
            self._speak("Apps file not found. Please set up the folder again.")
            self.prompt_user_for_apps_folder()

    def close_app(self, app_to_close):
        if not os.path.exists(self.apps_file):
            self._speak(f"Error: {self.apps_file} does not exist.")
            return

        with open(self.apps_file, 'r') as f:
            folder_path = f.read().strip()
        if not folder_path or not os.path.isdir(folder_path):
            self._speak(f"Error: Folder path {folder_path} is invalid.")
            return

        if folder_path and os.path.isdir(folder_path):
            app_path = os.path.join(folder_path, app_to_close)
            if not os.path.exists(app_path):
                app_path = os.path.join(folder_path, app_to_close + ".lnk")
            if not os.path.exists(app_path):
                app_path = os.path.join(folder_path, app_to_close + ".exe")
            if not os.path.exists(app_path):
                app_path = os.path.join(folder_path, app_to_close + ".url")
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == app_to_close.lower() or \
                    proc.info['name'].lower() == (app_to_close + ".exe").lower():
                    proc.terminate()
            except psutil.NoSuchProcess:

                return



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
                        self.open_was_said = False
                        break
                    elif 'close' in text:
                        self.close_was_said = True
                        app_name = self.splitting_text(text)
                        self.close_app(app_name)
                        self.close_was_said = False
                        break
                    elif text == "stop":
                        still_listening = False
                    else:
                        self._speak("I didn't catch a valid command. Please say 'open' or 'close'.")
                except sr.UnknownValueError:
                    self._speak("Sorry, I didn't understand. Could you repeat that?")

    def main_loop(self):
        self._speak("Hello, just speak my name and I will be able to assist you.")
        with sr.Microphone() as source:
            while True:
                try:
                    print("now here")
                    self.recognizer.adjust_for_ambient_noise(source)
                    word = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(word).lower()
                    if self.wake_word in text:
                        self.open_or_close_app()
                except sr.UnknownValueError:
                    None

    def prompt_user_for_apps_folder(self):
        folder_is_valid = False

        self._speak("Great to get started please create a folder that contains any shortcuts "
                    "or executable files of the applications you want me to control. Then, provide the folder path.")
        while folder_is_valid is False:
            folder_path = input("Enter the full path to the folder containing your apps: ")
            if os.path.isdir(folder_path):
                self._speak(f"Great! I'll now save the app paths in a file.")
                self.save_app_paths(folder_path)
                folder_is_valid = True
            else:
                self._speak("The folder path given does not exist. Please try again.")

    def save_app_paths(self, folder_path):
        try:
            with open("folder_that_leads_to_apps.txt", "w") as f:
                f.write(folder_path)
                self._speak("Folder path saved successfully.")
                self.main_loop()
        except Exception as e:
            self._speak("An error occurred")
            self.prompt_user_for_apps_folder()


jarvis = Jarvis()
