import tkinter
from typing import Dict
import platform

from tango_project_1_assignment_2.controller import Controller
#from controller import Controller on the robot's code


class KeyboardInput:
    # TODO: make class for keyboard input
    # local code (without a stream to another PC) doesn't seem to run any of the servos or motors despite printing
    # controller class is properly imported but nothing else happens
    # calls for motors seem correct though
    # back swivel engages when robot turns on. possibly has to do with the 0 index being motors normally?
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
        self.window.bind('<return>', self.stop_robot)
        #on local keyboard with robot, space is not recognized for space bar
        self.window.bind('<z>', self.drive_robot)
        self.window.bind('<c>', self.drive_robot)
        self.window.bind('<w>', self.drive_robot)
        self.window.bind('<s>', self.drive_robot)
        self.window.bind('<a>', self.drive_robot)
        self.window.bind('<d>', self.drive_robot)
        self.os = 'Linux' if platform.system() == 'Linux' else 'Windows'
        self.keydict = Dict[str: Dict[str:int]] = {"Linux": {'Up': 111,
                                                        'Down': 116,
                                                        'Left': 113,
                                                        'Right': 114,
                                                        'Return': 36,
                                                        'w': 25,
                                                        's': 39,
                                                        'a': 38,
                                                        'd': 40,
                                                        'z': 52,
                                                        'c': 54 },
                                            "Windows": {  'Up': 38,
                                                        'Down': 40,
                                                        'Left': 37,
                                                        'Right': 39,
                                                        'Return': 13,
                                                        'w': 87,
                                                        's': 83,
                                                        'a': 65,
                                                        'd': 68,
                                                        'z': 90,
                                                        'c': 67,},

                                            }

    def run(self):
        self.window.mainloop()

    def stop_robot(self, pressed_key) -> None:
        self.robot_controller.STOPDROPANDROLL()

    def drive_robot(self, pressed_key) -> None:
        """
        keyboard keycodes (win | linux)
        Up: 38 | 111
        Down: 40 | 116
        Left: 37 | 113
        Right: 39 | 114
        Space: 32 | unknown
        w: 87 | 25
        s: 83 | 39
        a: 65 | 38
        d: 68 | 40
        z: 90 | 52
        c: 67 | 54
        :param pressed_key:
        :return:
        """
        if pressed_key.keycode == self.keydict[self.os]['Up']:
            # up: forward
            self.robot_controller.forward()
        elif pressed_key.keycode == self.keydict[self.os]['Down']:
            # down: backwards
            self.robot_controller.reverse()
        elif pressed_key.keycode == self.keydict[self.os]['Left']:
            # left: left
            self.robot_controller.left()
        elif pressed_key.keycode == self.keydict[self.os]['Right']:
            # right: right
            self.robot_controller.right()
        elif pressed_key.keycode == self.keydict[self.os]['w']:
            # w: head up
            self.robot_controller.headnod(True)
        elif pressed_key.keycode == self.keydict[self.os]['s']:
            # s: head down
            self.robot_controller.headnod(False)
        elif pressed_key.keycode == self.keydict[self.os]['a']:
            # a: head left
            self.robot_controller.headshake(False)
        elif pressed_key.keycode == self.keydict[self.os]['d']:
            # d: head right
            self.robot_controller.headshake(True)
        elif pressed_key.keycode == self.keydict[self.os]['z']:
            # z: waist left
            self.robot_controller.turnwaist(False)
        elif pressed_key.keycode == self.keydict[self.os]['c']:
            # c: waist right
            self.robot_controller.turnwaist(True)
        print(pressed_key)
        pass

if __name__ == '__main__':
    keyboard_input: KeyboardInput = KeyboardInput()
    keyboard_input.run()
