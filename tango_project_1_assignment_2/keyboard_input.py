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
        self.window.bind('<space>', self.stop_robot)
        self.window.bind('<z>', self.drive_robot)
        self.window.bind('<c>', self.drive_robot)
        self.window.bind('<w>', self.drive_robot)
        self.window.bind('<s>', self.drive_robot)
        self.window.bind('<a>', self.drive_robot)
        self.window.bind('<d>', self.drive_robot)

    def run(self):
        self.window.mainloop()

    def stop_robot(self, pressed_key) -> None:
        if pressed_key.keycode == 32:
            # space
            self.robot_controller.STOPDROPANDROLL()

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
        if pressed_key.keycode == 38:
            # up: forward
            self.robot_controller.forward()
        elif pressed_key.keycode == 40:
            # down: backwards
            self.robot_controller.reverse()
        elif pressed_key.keycode == 37:
            # left: left
            self.robot_controller.left()
        elif pressed_key.keycode == 39:
            # right: right
            self.robot_controller.right()
        elif pressed_key.keycode == 87:
            # w
            pass
        elif pressed_key.keycode == 83:
            # s
            pass
        elif pressed_key.keycode == 65:
            # a
            pass
        elif pressed_key.keycode == 68:
            # d
            pass
        elif pressed_key.keycode == 90:
            # z
            pass
        elif pressed_key.keycode == 67:
            # c
            pass
        print(pressed_key)
        pass

if __name__ == '__main__':
    keyboard_input: KeyboardInput = KeyboardInput()
    keyboard_input.run()