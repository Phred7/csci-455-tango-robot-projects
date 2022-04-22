import platform
import time

from action_stategy import ActionStrategy
from controller import Controller


class Move(ActionStrategy):
    """
    Implements movement of this system forward and backwards.
    """

    def __init__(self, move_forward_bool: bool, time_to_move: int, speed: bool) -> None:
        super().__init__()
        self.move_forward_bool: bool = move_forward_bool
        self.time_to_move: int = time_to_move
        self.speed: bool = speed
        self.max_time: int = 10

    def execute_action(self, controller: Controller) -> None:
        """
        Causes the robot to move forward or backwards.
        :param controller: Controller object to control this system.
        :return: None.
        """
        if platform.system() == 'Windows':
            print(
                f"moving {'forward' if self.move_forward_bool else 'backwards'} for {self.time_to_move}seconds {'slow' if not self.speed else 'fast'}")
        else:
            if self.move_forward_bool:
                # controller.motor_velocity_counter = 4976
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()
                controller.forward()

                # controller.forward(controller.fivestepsofPOWER[1 if not self.speed else 0])
            elif not self.move_forward_bool:
                # controller.motor_velocity_counter = 7024
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()
                controller.reverse()

                # controller.reverse(controller.fivestepsofPOWER[3 if not self.speed else 4])
            if self.time_to_move > self.max_time:
                self.time_to_move = self.max_time
            time.sleep(self.time_to_move)
            controller.STOPDROPANDROLL()
        return
