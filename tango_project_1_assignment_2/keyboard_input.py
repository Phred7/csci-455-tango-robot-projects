import tkinter

from tango_project_1_assignment_2.controller import Controller


class KeyboardInput:
    # TODO: make class for keyboard input
    # Hunter uses a window for keyboard controlling on the video, not sure how that's supposed to work.
    # Imported tkinter for later use. Guessing we need to be active on a specific window to record key inputs w/tkinter
    # Hunter doesn't have methods, he just has an if else chain for each keycode (23:49 on week 6 friday video)

    def __init__(self) -> None:
        self.robot_controller: Controller = Controller()
        self.window = tkinter.Tk()
        self.window.bind('<Up>', self.drive_robot)
        self.window.bind('<Down>', self.drive_robot)
        self.window.bind('<Left>', self.drive_robot)
        self.window.bind('<Right>', self.drive_robot)
        self.window.bind('<space>', self.drive_robot)
        self.window.bind('<z>', self.drive_robot)
        self.window.bind('<c>', self.drive_robot)
        self.window.bind('<w>', self.drive_robot)
        self.window.bind('<s>', self.drive_robot)
        self.window.bind('<a>', self.drive_robot)
        self.window.bind('<d>', self.drive_robot)

    def run(self):
        self.window.mainloop()

    def drive_robot(self, pressed_key) -> None:
        """
        keyboard keycodes
        Up: 38
        Down: 40
        Left: 37
        Right: 39
        Space: 32
        w: 87
        s: 83
        a: 65
        d: 68
        z: 90
        c: 67
        :param pressed_key:
        :return:
        """
        print(pressed_key)
        pass

if __name__ == '__main__':
    keyboard_input: KeyboardInput = KeyboardInput()
    keyboard_input.run()
