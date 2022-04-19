from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('popup.kv')


class HeadPopUp(Widget):
    checks = []

    def checkbox_click(self, instance, value, choice):
        if value == True:
            HeadPopUp.checks.append(choice)
            tops = ''
            for x in HeadPopUp.checks:
                tops = f'{tops} {x}'
            self.ids.output.text = f'you chose {tops}'
        else:
            HeadPopUp.checks.remove(choice)


class AppBuilder(App):
    def build(self):
        return HeadPopUp()


if __name__ == '__main__':
    AppBuilder().run()
