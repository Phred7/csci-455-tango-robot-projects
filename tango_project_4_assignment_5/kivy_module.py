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


class StressCanvasApp(App):
    add = 0

    def add_rects(self, label, wid, count, *largs):
        print("adding", count)
        label.text = str(int(label.text) + count)
        with wid.canvas:
            for x in range(count):
                Color(r(), 1, 1, mode='hsv')
                Rectangle(pos=(r() * wid.width + wid.x,
                               r() * wid.height + wid.y), size=(20, 20))

    def double_rects(self, label, wid, *largs):
        count = int(label.text)
        self.add_rects(label, wid, count, *largs)

    def reset_rects(self, label, wid, *largs):
        label.text = '0'
        self.add = 0
        wid.canvas.clear()

    def addVals(self, val, *largs):
        self.add = self.add + val
        print(self.add)

    def mulVals(self, val, *largs):
        self.add = self.add * val
        print(self.add)

    def build(self):
        wid = Widget()
        label = Label(text='0')
        self.img = Image(source = 'spider.jpg')
        btn_turn = Button(text='Turn',
                          on_press=partial(self.addVals, 100))

        btn_head = Button(text='Head',
                          on_press=partial(self.addVals, 500))

        btn_waist = Button(text='Waist',
                           on_press=partial(self.mulVals, 2))

        btn_move = Button(text='Move',
                          on_press=partial(self.mulVals, 0.5))
        btn_speech = Button(text='Speech',
                            on_press=partial(self.mulVals, 0.5))

        btn_delete = Button(text=' Delete',
                            on_press=partial(self.reset_rects, label, wid))

        btn_play = Button(text='Play',
                          on_press=partial(self.add_rects, label, wid, self.add))

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
