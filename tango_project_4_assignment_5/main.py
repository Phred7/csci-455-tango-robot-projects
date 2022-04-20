import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

FruitsSellected = []

class Widgets(Widget):
    def btn(self):
        show_popup()

class P(FloatLayout):
    def checkboxes_click(self, instance, value, text):
        if value:
            print(f"Select {text}")
            self.myvar = FruitsSellected
            # Close
            if text == 'FINISH':
                print(FruitsSellected)
                self.save()
                App.get_running_app().stop()
                return FruitsSellected

            FruitsSellected.append(str(text))

        else:
            print(f"UnSelect {text}")
            FruitsSellected.remove(str(text))


class MyApp(App):
    def build(self):
        return Widgets()


def show_popup():
    show = P()
    # layout = Checkboxes()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(600,600))

    popupWindow.open()


if __name__ == "__main__":
    MyApp().run()