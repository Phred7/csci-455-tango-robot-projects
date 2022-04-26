from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock

Config.set('graphics', 'resizable', True)

class BackgroundApp(App):
    from kivy.config import Config
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '400')

    @staticmethod
    def update_img(self):
        try:
            with open("images/picture.txt", "r") as txt_file:
                img.source = 'images/' + str(txt_file.readline())
        except IOError:
            img.source = 'images/gray.jpg'

    def build(self):
        global img

        Clock.schedule_interval(self.update_img, 1)

        img = Image(source='images/gray.jpg', allow_stretch=True, keep_ratio=False)

        rect = BoxLayout(orientation='horizontal', padding=50)
        rect.add_widget(img)

        root = BoxLayout(orientation='horizontal')
        root.add_widget(rect)

        return root

if __name__ == '__main__':
    BackgroundApp().run()
