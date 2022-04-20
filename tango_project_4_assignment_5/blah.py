from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.widget import Widget
import kivy
kivy.require('1.10.1')

from kivy.uix.popup import Popup


FruitsSellected = []


class Checkboxes(Widget):

  def checkboxes_click(self, instance, value, text):
    if value:
      print(f"Select {text}")
      self.myvar = FruitsSellected
      #Close
      if text == 'FINISH':
        print(FruitsSellected)
        self.save()
        App.get_running_app().stop()
        return FruitsSellected

      FruitsSellected.append(str(text))

    else:
      print(f"UnSelect {text}")
      FruitsSellected.remove(str(text))

  def save(self):
    with open("allergenlist.txt", "w") as fobj:
      fobj.write(str(self.myvar))




class CheckBoxesApp(App):
  def build(self):
    return Checkboxes()


class YourApp(App):

    def build(self):
        # Define a grid layout for this App
        self.layout = GridLayout(cols=1, padding=10)

        # Don't worry about this button, just a place holder
        self.button = Button(text="TAKE PICTURE")
        self.layout.add_widget(self.button)
        # Add a button
        self.button2 = Button(text="SELECT")
        self.layout.add_widget(self.button2)        # Add a button

        # Attach a callback for the button press event
        self.button.bind(on_press=self.onButtonPress)
        self.button2.bind(on_press=self.onButtonPress3)

        return self.layout

    #Place Holder don't worry about this either
    def onButtonPress(self, button):

        layout = GridLayout(cols=1, padding=10)

        popupLabel = Label(text="TAKE PICTURE")
        closeButton = Button(text="Close the pop-up")

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        # Instantiate the modal popup and display
        popup = Popup(title='TAKE PICTURE',
                      content=layout)
        popup.open()

        # Attach close button press
        closeButton.bind(on_press=popup.dismiss)



    def onButtonPress3(self, button):


        layout = Checkboxes()
        popup3 = Popup(title='SELECT', content=layout)
        popup3.open()


if __name__ == '__main__':
    YourApp().run()