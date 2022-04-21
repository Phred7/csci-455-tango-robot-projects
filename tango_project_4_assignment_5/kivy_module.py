"""
Canvas stress
=============

This example tests the performance of our Graphics engine by drawing large
numbers of small squares. You should see a black canvas with buttons and a
label at the bottom. Pressing the buttons adds small colored squares to the
canvas.
"""

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle
from random import random as r
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from action import Action
from tango_project_4_assignment_5.actions.head import Head

# full of tuples (ActionObject, string pictureurl)
globalarray = []


class HeadPopup(FloatLayout):
    Choices = []

    def checkboxes_click(self, instance, value, text):
        if value:
            self.Choices.append(str(text))
        else:
            self.Choices.remove(str(text))

    def button_press(self, idk):
        print(self.Choices)
        globalarray.append((Action(Head(self.Choices[0])), 'holderstring'))
        self.Choices = []
        print(self.Choices)
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
        # TODO save the entered info here
        self.Choices = []
        print(self.Choices)
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
        # TODO save the entered info here
        self.Choices = []
        print(self.Choices)
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
        print(self.Choices)
        # TODO save the entered info here
        self.Choices = []
        print(self.Choices)
        self.parent.parent.parent.dismiss()


def show_Turn(trash):
    content = TurnPopup()
    popup = Popup(title="Turn Action", content=content, size_hint=(None, None), size=(600, 1000))
    popup.open()


class SpeechPopup(FloatLayout):
    Choices = []

    def checkboxes_click(self, instance, value, text):
        if value:
            self.Choices.append(str(text))
        else:
            self.Choices.remove(str(text))

    def button_press(self, idk):
        print(self.Choices)
        # TODO save the entered info here
        self.Choices = []
        print(self.Choices)
        self.parent.parent.parent.dismiss()


def show_Speech(trash):
    content = SpeechPopup()
    popup = Popup(title="Speech Action", content=content, size_hint=(None, None), size=(600, 600))
    popup.open()


class StressCanvasApp(App):

    def build(self):
        label = Label(text='0')
        self.img = Image(source='spider.jpg')

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
        # btn_delete.bind(on_press=show_Speech)

        btn_play = Button(text='Play')
        # btn_play.bind(on_press=show_Speech)

        layout = BoxLayout(size_hint=(1, None), orientation='horizontal')
        layout.add_widget(btn_head)
        layout.add_widget(btn_speech)
        layout.add_widget(btn_move)
        layout.add_widget(btn_waist)
        layout.add_widget(btn_turn)
        layout.add_widget(btn_delete)
        layout.add_widget(btn_play)
        layout.add_widget(label)

        root = BoxLayout(orientation='vertical')
        # root.add_widget(box1)
        # root.add_widget(box2)
        # root.add_widget(box3)
        # root.add_widget(box4)
        # root.add_widget(box5)
        # root.add_widget(box6)
        # root.add_widget(box7)
        # root.add_widget(box8)
        root.add_widget(layout)

        return root


if __name__ == '__main__':
    StressCanvasApp().run()
