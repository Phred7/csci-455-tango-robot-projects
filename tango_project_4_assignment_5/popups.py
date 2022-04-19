from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('popup.kv')

class HeadPopUp(Widget):
    pass

class AppBuilder(App):
    def build(self):
        return HeadPopUp()

if __name__ = '__main__'
    AppBuilder().run()