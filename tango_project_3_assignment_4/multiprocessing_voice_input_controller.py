"""Multiprocessing Controller"""
import multiprocessing
from multiprocessing import Process, Queue
from typing import Dict, List
import speech_recognition as sr
import tkinter
import pyttsx3

from controller import Controller
from tango_chat_file_parser import TangoChatFileParser


class MultiprocessingVoiceInputController:

    def __init__(self) -> None:
        self.tts_process: Process
        self.queue: Queue[str] = Queue()
        self.lock: multiprocessing.Lock = multiprocessing.Lock()
        self.processes: Dict["str": Process] = {"tts": Process(target=self.tts, args=(), name=f"tts_process"),
                                                "controller": Process(target=self.controller, args=(), name=f"controller_process")}
        self.processes_running: bool = False

    def run(self) -> None:
        self.processes_running = True
        try:
            for process in self.processes.values():
                process.start()
        except Exception as e:
            self.processes_running = False
            print(e)
        for process in self.processes.values():
            process.join()

    def tts(self) -> None:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 150)
        voices = tts_engine.getProperty('voices')
        tts_engine.setProperty('voice', voices[2].id)
        while self.processes_running:
            if not self.queue.empty():
                pop: str = self.queue.get(timeout=1)
                self.lock.acquire()
                print(f"{multiprocessing.process.current_process().name}: got \'{pop}\' from queue")
                self.lock.release()
                tts_engine.say(pop)
                tts_engine.runAndWait()
        pass

    def controller(self) -> None:
        robot_controller: Controller = Controller()
        window = tkinter.Tk()
        tcfp: TangoChatFileParser = TangoChatFileParser(chat_file="tango_chat.txt")
        listening = True
        while listening and self.processes_running:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dyanmic_energythreshhold = 3000
                # r.operation_timeout = 8
                # r.phrase_threshold = 0.15

                try:
                    self.__print("listening")
                    audio = r.listen(source, timeout=8)
                    self.__print("got audio")
                    user_input = r.recognize_google(audio)
                    self.queue.put(tcfp.user_input(user_input))
                    self.__print(user_input)
                    array_of_words: List[str] = user_input.split()

                except sr.UnknownValueError:
                    string: str = "Sorry good chap but I'm a little dull and didn't quite pick that one up."
                    self.queue.put("Fool of a Took")
                    self.__print(string)
                except sr.WaitTimeoutError:
                    self.__print("Listen timeout exceeded")

    def __print(self, print_str: str) -> None:
        self.lock.acquire()
        print(print_str)
        self.lock.release()

if __name__ == "__main__":
    mvic: MultiprocessingVoiceInputController = MultiprocessingVoiceInputController()
    mvic.run()
    pass