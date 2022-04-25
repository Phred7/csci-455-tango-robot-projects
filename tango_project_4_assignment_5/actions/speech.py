import platform
import random
from typing import List

from action_stategy import ActionStrategy
from controller import Controller
import speech_recognition
import pyttsx3


class Speech(ActionStrategy):
    """
    Implements speech input and output of this system.
    """

    def __init__(self, speech_input_bool: bool, speech_string: str = ""):  # can pass function to add to multiprocessing queue as a arg. Then call w/ arg(string)
        super().__init__()
        self.speech_input_bool: bool = speech_input_bool
        self.speech_string: str = speech_string

    def execute_action(self, controller: Controller) -> None:
        """
        Causes the robot to say something or wait for user input.
        :param controller: Controller object to control this system.
        :return: None.
        """
        if platform.system() == 'Windows':
            print("Getting a speech input" if self.speech_input_bool else f"Outputting: {self.speech_string}")
        else:
            if self.speech_input_bool:
                self.__say("Speak when ready.")
                self.speech_string = Speech.__get_speech()
                self.__say(f"Got the string \'{self.speech_string}\'.")
            else:
                if self.speech_string != "":
                    Speech.__say(self.speech_string)
        return

    @staticmethod
    def __say(string: str) -> None:
        text_to_speech_engine = pyttsx3.init()
        text_to_speech_engine.setProperty('rate', 150)
        voices = text_to_speech_engine.getProperty('voices')
        text_to_speech_engine.setProperty('voice', voices[2].id)
        text_to_speech_engine.say(string)
        text_to_speech_engine.runAndWait()

    @staticmethod
    def __get_speech() -> str:
        listening = True
        return_string: str = ""
        while listening:
            with speech_recognition.Microphone() as source:
                speech_recognizer = speech_recognition.Recognizer()
                speech_recognizer.adjust_for_ambient_noise(source)
                speech_recognizer.dynamic_energy_threshold = 3000
                # r.operation_timeout = 8
                # r.phrase_threshold = 0.15

                try:
                    print("listening")
                    audio = speech_recognizer.listen(source, timeout=8)
                    print("got audio")
                    user_input = speech_recognizer.recognize_google(audio)
                    return user_input

                except speech_recognition.UnknownValueError:
                    print("Unknown input.")
                    strings: List[str] = ["nope", "try again", "you're speaking too quietly", "what'd you say?", "nani", "unrecognizable input"]
                    Speech.__say(random.choice(strings))
                except speech_recognition.WaitTimeoutError:
                    print("Listen timeout exceeded.")

            if return_string != "":
                listening = False

        return return_string


if __name__ == "__main__":
    pass
