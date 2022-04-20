import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

class Widgets(Widget):
    def btn(self):
        show_popup()

class P(FloatLayout):
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

def show_popup():
    content = P()

    popup = Popup(title="Please select from below", content=content, size_hint=(None,None),size=(600,600))
    # content.bind(on_press=popup.dismiss)
    popup.open()

class MyApp(App):
    def build(self):
        return Widgets()


if __name__ == "__main__":
    MyApp().run()