import platform
from time import sleep

from action_stategy import ActionStrategy
from controller import Controller


class Head(ActionStrategy):
    """
    Implements movement of the head for this system.
    """

    def __init__(self, direction_to_move: str) -> None:
        super().__init__()
        self.direction_to_move: str = direction_to_move

    def execute_action(self, controller: Controller) -> None:
        """
        Causes the robot to move the head in a defined direction.
        :param controller: Controller object to control this system.
        :return: None.
        """
        print(f"head direction: {self.direction_to_move}")
        if platform.system() == 'Windows':
            print("Windows")
        else:
            if self.direction_to_move == "Up":
                controller.headnod(True)
            elif self.direction_to_move == "Down":
                controller.headnod(False)
            elif self.direction_to_move == "Left":
                controller.headshake(False)
            elif self.direction_to_move == "Right":
                controller.headshake(True)
            else:
                print("head movement direction not recognized.")
            sleep(2)
        return
