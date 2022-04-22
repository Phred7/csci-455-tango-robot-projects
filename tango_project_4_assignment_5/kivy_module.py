"""
Canvas stress
=============

This example tests the performance of our Graphics engine by drawing large
numbers of small squares. You should see a black canvas with buttons and a
label at the bottom. Pressing the buttons adds small colored squares to the
canvas.
"""
from typing import Tuple, List

from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle
from random import random as r
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivymd.uix.spinner import MDSpinner

from action import Action
import speech_recognition
import pyttsx3
from tango_project_4_assignment_5.actions.head import Head

# full of tuples (Action, string pictureurl)
from tango_project_4_assignment_5.actions.move import Move
from tango_project_4_assignment_5.actions.speech import Speech
from tango_project_4_assignment_5.actions.turn import Turn
from tango_project_4_assignment_5.actions.waist import Waist
from tango_project_4_assignment_5.controller import Controller

connies_global_array: List[Tuple[Action, str]] = []


class HeadPopup(FloatLayout):
    Choices = []

    def checkboxes_click(self, instance, value, text):
        if value:
            self.Choices.append(str(text))
        else:
            self.Choices.remove(str(text))

    def button_press(self, idk):
        print(self.Choices)
        connies_global_array.append((Action(Head(self.Choices[0])), 'spider.jpg'))
        self.Choices = []
        print(connies_global_array)
        self.parent.parent.parent.dismiss()


def show_Head(trash):
    content = HeadPopup()
    popup = Popup(title="Head Action", content=content, size_hint=(None, None), size=(600, 600))
    popup.open()


class WaistPopup(FloatLayout):
    Choices = []

    def checkboxes_click(self, instance, value, text):
        if value:
            self.Choices.append(str(text))
        else:
            self.Choices.remove(str(text))

    def button_press(self, idk):
        print(self.Choices)
        if self.Choices[0] == "Left":
            connies_global_array.append((Action(Waist(True)), 'holderstring'))
        else:
            connies_global_array.append((Action(Waist(False)), 'holderstring'))
        self.Choices = []
        print(connies_global_array)
        self.parent.parent.parent.dismiss()


def show_Waist(trash):
    content = WaistPopup()
    popup = Popup(title="Waist Action", content=content, size_hint=(None, None), size=(600, 600))
    popup.open()


class MovePopup(FloatLayout):
    Choices = []

    def checkboxes_click(self, instance, value, text):
        if value:
            self.Choices.append(str(text))
        else:
            self.Choices.remove(str(text))

    def button_press(self, idk):

        print(self.Choices)
        forward = False
        speed = False
        if self.Choices[0] == "Forward":
            forward = True
        if self.Choices == "Fast":
            speed = True
        connies_global_array.append((Action(Move(forward, self.choices[1], speed)), 'holderstring'))
        self.Choices = []
        print(connies_global_array)
        self.parent.parent.parent.dismiss()


def show_Move(trash):
    content = MovePopup()
    popup = Popup(title="Move Action", content=content, size_hint=(None, None), size=(600, 1000))
    popup.open()


class TurnPopup(FloatLayout):
    Choices = []

    def checkboxes_click(self, instance, value, text):
        if value:
            self.Choices.append(str(text))
        else:
            self.Choices.remove(str(text))

    def button_press(self, idk):
        # StressCanvasApp.image_callback(StressCanvasApp.rects,'spider.jpg')
        # TODO find some way to access image widgets (method variables) from other classes (i might also just be stupid)
        print(self.Choices)
        left = False
        if self.Choices[0] == "Left":
            left = True
        connies_global_array.append((Action(Turn(left, self.choices[1])), 'holderstring'))
        self.Choices = []
        print(connies_global_array)
        self.parent.parent.parent.dismiss()


def show_Turn(trash):
    content = TurnPopup()
    popup = Popup(title="Turn Action", content=content, size_hint=(None, None), size=(600, 1000))
    popup.open()


class SpeechPopup(FloatLayout):
    Choices = []
    speech_string: str = ""

    def checkboxes_click(self, _instance, value, text):
        if value:
            self.Choices.append(str(text))
        else:
            self.Choices.remove(str(text))

    def button_press(self, _idk):
        print(self.Choices)
        input = False
        if self.Choices[0] == "Input":
            input = True
        connies_global_array.append((Action(Speech(input, self.speech_string)), ""))
        self.Choices = []
        print(connies_global_array)
        self.parent.parent.parent.dismiss()

    def record_button(self, _button_value) -> None:
        self.speech_string = self.__get_speech()

    def __get_speech(self) -> str:
        user_input: str = ""
        listening = True
        while listening:
            with speech_recognition.Microphone() as source:
                recognizer = speech_recognition.Recognizer()
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                # recognizer.operation_timeout = 8
                # recognizer.phrase_threshold = 0.15
                try:
                    print("listening")
                    audio = recognizer.listen(source, timeout=8)
                    print("got audio")
                    user_input = recognizer.recognize_google(audio)

                except speech_recognition.UnknownValueError:
                    print("Unknown voice input")
                except speech_recognition.WaitTimeoutError:
                    print("Listen timeout exceeded")

            if user_input != "":
                listening = False
        return user_input


def show_Speech(trash):
    content = SpeechPopup()
    popup = Popup(title="Speech Action", content=content, size_hint=(None, None), size=(600, 600))
    popup.open()


class DeletePopup(FloatLayout):
    Choices = []

    def checkboxes_click(self, instance, value, text):
        if value:
            self.Choices.append(str(text))
        else:
            self.Choices.remove(str(text))

    def button_press(self, idk):
        global connies_global_array
        if self.Choices[0] == 'All':
            print('tired to delete last all')
            connies_global_array = []
        if self.Choices[0] == 'Last':
            print('tired to delete last one')
            connies_global_array.pop()
        print(connies_global_array)
        self.parent.parent.parent.dismiss()


def show_Delete(trash):
    content = DeletePopup()
    popup = Popup(title="ARE YOU SURE YOU WANT TO DELETE?", content=content, size_hint=(None, None), size=(600, 600))
    popup.open()


def play(_button_value) -> None:
    animation = Animation(pos=(100, 100), t='out_bounce')
    animation += Animation(pos=(200, 100), t='out_bounce')
    animation &= Animation(size=(500, 500))
    animation += Animation(size=(100, 50))
    # robot_controller: Controller = Controller()
    # for action, string in connies_global_array:
    #     action.execute_action(robot_controller)
    animation.start(_button_value)

    e = Label(text= 'test')
    e.canvas()


Config.set('graphics', 'resizable', True)

class StressCanvasApp(App):

    def update_img1(trash, blah):
        try:
            connies_global_array[0]
            img.source = connies_global_array[0][1]
        except IndexError:
            img.source = 'gray.jpg'

    def update_img2(trash, blah):
        try:
            connies_global_array[1]
            img2.source = connies_global_array[1][1]
        except IndexError:
            img2.source = 'gray.jpg'

    def update_img3(trash, blah):
        try:
            connies_global_array[2]
            img3.source = connies_global_array[2][1]
        except IndexError:
            img3.source = 'gray.jpg'

    def update_img4(trash, blah):
        try:
            connies_global_array[3]
            img4.source = connies_global_array[3][1]
        except IndexError:
            img4.source = 'gray.jpg'

    def update_img5(trash, blah):
        try:
            connies_global_array[4]
            img5.source = connies_global_array[4][1]
        except IndexError:
            img5.source = 'gray.jpg'

    def update_img6(trash, blah):
        try:
            connies_global_array[5]
            img6.source = connies_global_array[5][1]
        except IndexError:
            img6.source = 'gray.jpg'

    def update_img7(trash, blah):
        try:
            connies_global_array[6]
            img7.source = connies_global_array[6][1]
        except IndexError:
            img7.source = 'gray.jpg'

    def update_img8(trash, blah):
        try:
            connies_global_array[7]
            img8.source = connies_global_array[7][1]
        except IndexError:
            img8.source = 'gray.jpg'

    def image_callback(rectImage, value):
        rectImage.source = value

    def build(self):
        label = Label(text='0')
        global img
        global img2
        global img3
        global img4
        global img5
        global img6
        global img7
        global img8

        Clock.schedule_interval(self.update_img1, 1)
        Clock.schedule_interval(self.update_img2, 1)
        Clock.schedule_interval(self.update_img3, 1)
        Clock.schedule_interval(self.update_img4, 1)
        Clock.schedule_interval(self.update_img5, 1)
        Clock.schedule_interval(self.update_img6, 1)
        Clock.schedule_interval(self.update_img7, 1)
        Clock.schedule_interval(self.update_img8, 1)



        img = Image(source='gray.jpg', allow_stretch=True, keep_ratio=False, size_hint_y=0.5, pos_hint={'top': 0.75})
        img2 = Image(source='gray.jpg', allow_stretch=True, keep_ratio=False, size_hint_y=0.5, pos_hint={'top': 0.75})
        img3 = Image(source='gray.jpg', allow_stretch=True, keep_ratio=False, size_hint_y=0.5, pos_hint={'top': 0.75})
        img4 = Image(source='gray.jpg', allow_stretch=True, keep_ratio=False, size_hint_y=0.5, pos_hint={'top': 0.75})
        img5 = Image(source='gray.jpg', allow_stretch=True, keep_ratio=False, size_hint_y=0.5, pos_hint={'top': 0.75})
        img6 = Image(source='gray.jpg', allow_stretch=True, keep_ratio=False, size_hint_y=0.5, pos_hint={'top': 0.75})
        img7 = Image(source='gray.jpg', allow_stretch=True, keep_ratio=False, size_hint_y=0.5, pos_hint={'top': 0.75})
        img8 = Image(source='gray.jpg', allow_stretch=True, keep_ratio=False, size_hint_y=0.5, pos_hint={'top': 0.75})

        btn_head = Button(text='Head')
        btn_head.bind(on_press=show_Head)

        btn_waist = Button(text='Waist')
        btn_waist.bind(on_press=show_Waist)

        btn_move = Button(text='Move')
        btn_move.bind(on_press=show_Move)

        btn_turn = Button(text='Turn')
        btn_turn.bind(on_press=show_Turn)

        btn_speech = Button(text='Speech')
        btn_speech.bind(on_press=show_Speech)

        btn_delete = Button(text='Delete')
        btn_delete.bind(on_press=show_Delete)

        btn_play = Button(text='Play')
        btn_play.bind(on_press=play)

        layout = BoxLayout(size_hint=(0.2, 1), orientation='vertical', padding=[0, 10, 0, 10])

        layout.add_widget(btn_head)
        layout.add_widget(btn_speech)
        layout.add_widget(btn_move)
        layout.add_widget(btn_waist)
        layout.add_widget(btn_turn)
        layout.add_widget(btn_delete)
        layout.add_widget(btn_play)
        # layout.add_widget(label)

        rects = BoxLayout(size_hint=(0.8, 1), orientation='horizontal', padding=[50, 0, 50, 0], spacing=10)
        rects.add_widget(img)
        rects.add_widget(img2)
        rects.add_widget(img3)
        rects.add_widget(img4)
        rects.add_widget(img5)
        rects.add_widget(img6)
        rects.add_widget(img7)
        rects.add_widget(img8)

        root = BoxLayout(orientation='horizontal')
        root.add_widget(layout)
        root.add_widget(rects)

        return root


if __name__ == '__main__':
    StressCanvasApp().run()
