import time

from tango_project_4_assignment_5.action_stategy import ActionStrategy
from tango_project_4_assignment_5.controller import Controller


class Move(ActionStrategy):
    """
    Implements movement of this system forward and backwards.
    """

    def __init__(self, move_forward_bool: bool, time_to_move: int, speed: bool) -> None:
        super().__init__()
        self.move_forward_bool: bool = move_forward_bool
        self.time_to_move: int = time_to_move
        self.speed: bool = speed
        self.max_time: int = 5

    def execute_action(self, controller: Controller) -> None:
        """
        Causes the robot to move forward or backwards.
        :param controller: Controller object to control this system.
        :return: None.
        """
        if self.move_forward_bool:
            controller.forward(controller.fivestepsofPOWER[1 if not self.speed else 0])
        elif not self.move_forward_bool:
            controller.reverse(controller.fivestepsofPOWER[3 if not self.speed else 4])
        if self.time_to_move > self.max_time:
            self.time_to_move = self.max_time
        time.sleep(self.time_to_move)
        return