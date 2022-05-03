import platform
from typing import List

import random
import speech_recognition
import pyttsx3


class Speech:
    """
    Implements Text To Speech and a Speech Recognizer.
    """

    @staticmethod
    def say(string: str) -> None:
        text_to_speech_engine = pyttsx3.init()
        text_to_speech_engine.setProperty('rate', 150)
        if platform.system() == "Windows" or platform.system() == "Darwin":
            print(f"Speech: {string}")
        else:
            voices = text_to_speech_engine.getProperty('voices')
            text_to_speech_engine.setProperty('voice', voices[2].id)
            text_to_speech_engine.say(string)
            text_to_speech_engine.runAndWait()

    @staticmethod
    def get_speech() -> str:
        if platform.system() == "Windows" or platform.system() == "Darwin":
            return input("Get Speech. Enter you input here: ")
        else:
            listening = True
            while listening:
                with speech_recognition.Microphone() as source:
                    speech_recognizer = speech_recognition.Recognizer()
                    speech_recognizer.adjust_for_ambient_noise(source)
                    speech_recognizer.dynamic_energy_threshold = 3000
                    speech_recognizer.operation_timeout = 8
                    speech_recognizer.phrase_threshold = 0.15
                    try:
                        if platform.system() == "Windows":
                            print("fictitiously got audio for windows")
                            return "fictitious"
                        print("listening")
                        audio = speech_recognizer.listen(source, timeout=8)
                        print("got audio")
                        user_input = speech_recognizer.recognize_google(audio)
                        print(user_input)
                        return user_input
                    except speech_recognition.UnknownValueError:
                        print("Unknown input.")
                        strings: List[str] = ["nope", "try again", "lol what", "what did you say?", "nani",
                                              "unrecognizable input", "pardon", "excuse me", "sorry, I missed what you said just then"]
                        Speech.say(random.choice(strings))
                    except speech_recognition.WaitTimeoutError:
                        print("Listen timeout exceeded.")
                        Speech.say("Listen timeout exceeded.")
