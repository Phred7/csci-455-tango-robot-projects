import time

from action_stategy import ActionStrategy
from controller import Controller


class Turn(ActionStrategy):
    """
    Implements turning for this system.
    """

    def __init__(self, turn_left_bool: bool, turn_time: int) -> None:
        super().__init__()
        self.turn_left_bool: bool = turn_left_bool
        self.turn_time: int = turn_time

    def execute_action(self, controller: Controller) -> None:
        """
        Causes the robot to turn for a given amount of time.
        :param controller: Controller object to control this system.
        :return: None.
        """
        if self.turn_left_bool:
            controller.left_drive_servos()
            controller.left_drive_servos()
            controller.left_drive_servos()
            controller.left_drive_servos()
            controller.left_drive_servos()
            controller.left_drive_servos()
            controller.left_drive_servos()
            controller.left_drive_servos()
            controller.left_drive_servos()
            controller.left_drive_servos()
            # controller.motor_turn_velocity_counter = controller.fivestepsofPOWER[3]
            controller.left_drive_servos()
        else:
            controller.right_drive_servos()
            controller.right_drive_servos()
            controller.right_drive_servos()
            controller.right_drive_servos()
            controller.right_drive_servos()
            controller.right_drive_servos()
            controller.right_drive_servos()
            controller.right_drive_servos()
            controller.right_drive_servos()
            controller.right_drive_servos()
            # controller.motor_turn_velocity_counter = controller.fivestepsofPOWER[1]
            controller.right_drive_servos()
        time.sleep(self.turn_time)
        controller.STOPDROPANDROLL()
        return
