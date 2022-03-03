import tkinter

from tango_project_1_assignment_2.controller import Controller


class KeyboardInput:
    # TODO: make class for keyboard input
    # Hunter uses a window for keyboard controlling on the video, not sure how that's supposed to work.
    # Imported tkinter for later use. Guessing we need to be active on a specific window to record key inputs w/tkinter
    # Hunter doesn't have methods, he just has an if else chain for each keycode (23:49 on week 6 friday video)

    def __init__(self) -> None:
        window = tkinter.Tk()
        window.bind('<Up>', self.drive_robot)
        window.bind('<Down>', self.drive_robot)
        window.bind('<Left>', self.drive_robot)
        window.bind('<Right>', self.drive_robot)
        window.mainloop()

    def drive_robot(self, pressed_key) -> None:
        pass