"""Multiprocessing Controller"""
import multiprocessing
from multiprocessing import Process, Queue
from typing import Dict, List
import speech_recognition as sr
import tkinter

from controller import Controller


class MultiprocessingVoiceInputController:

    def __init__(self) -> None:
        self.tts_process: Process
        self.queue: Queue[str] = Queue()
        self.lock: multiprocessing.Lock = multiprocessing.Lock()
        self.processes: Dict["str": Process] = {"tts": Process(target=self.tts, args=(), name=f"tts_process"),
                                                "controller": Process(target=self.controller, args=(), name=f"tts_process")}
        self.processes_running: bool = True

    def tts(self) -> None:
        while self.processes_running:
            if not self.queue.empty():
                pop: str = self.queue.get(timeout=1)

        pass

    def controller(self) -> None:
        robot_controller: Controller = Controller()
        window = tkinter.Tk()

        listening = True
        while listening:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dyanmic_energythreshhold = 3000
                # r.operation_timeout = 8
                # r.phrase_threshold = 0.15

                try:
                    print("listening")
                    audio = r.listen(source, timeout=8)
                    print("Got audio")
                    user_input = r.recognize_google(audio)
                    self.queue.put(user_input)
                    print(user_input)
                    array_of_words: List[str] = user_input.split()

                except sr.UnknownValueError:
                    print("Don't knoe that werd")
                except sr.WaitTimeoutError:
                    print("Listen timeout exceeded")
