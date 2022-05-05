import platform
from time import sleep

from typing import Callable
from controller import Controller


class ControllerInterface:
    """
    Implements the Controller for a robot and encapsulates most of the gore implementation details associated with that.
    """

    def __init__(self) -> None:
        self.__robot_controller: Controller = Controller()
        self.__platform = platform.system()
        self.__max_time: float = 10.0
        self.__forward_backwards_number_of_repeated_calls: int = 16
        self.__turning_number_of_repeated_calls: int = 20

    def __start_servo_controller(self) -> None:
        self.__robot_controller.reset_joints()
        self.__call_action_and_stop(self.__robot_controller.forward, "restart servo controller", number_of_iterations=4, number_of_seconds=0.5)

    def __wait_for_time(self, seconds: float):
        if seconds > self.__max_time:
            seconds = self.__max_time
        sleep(seconds)

    def stop(self) -> None:
        self.__robot_controller.STOPDROPANDROLL()

    def __call_action_and_stop(self, method: Callable, string_representation: str, number_of_iterations: int, number_of_seconds: float):
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"{string_representation} for {number_of_seconds} seconds")
        else:
            for _ in range(0, number_of_iterations):
                method()
            self.__wait_for_time(number_of_seconds)
            self.stop()
        pass

    def forward(self, number_of_seconds: float) -> None:
        self.__call_action_and_stop(self.__robot_controller.forward, "drive forward", self.__forward_backwards_number_of_repeated_calls, number_of_seconds)

    def backwards(self, number_of_seconds: float) -> None:
        self.__call_action_and_stop(self.__robot_controller.reverse, "drive backwards", self.__forward_backwards_number_of_repeated_calls, number_of_seconds)

    def turn_left(self, number_of_seconds: float) -> None:
        self.__call_action_and_stop(self.__robot_controller.left_drive_servos, "turn left",
                                    self.__forward_backwards_number_of_repeated_calls, number_of_seconds)

    def turn_right(self, number_of_seconds: float) -> None:
        self.__call_action_and_stop(self.__robot_controller.right_drive_servos, "turn right",
                                    self.__forward_backwards_number_of_repeated_calls, number_of_seconds)

    def left_arm_up(self) -> None:
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"left arm up")
        else:
            self.__robot_controller.left_arm(True)
            sleep(0.05)

    def left_arm_down(self) -> None:
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"left arm down")
        else:
            self.__robot_controller.left_arm(False)
            sleep(0.05)

    def right_arm_up(self) -> None:
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"right arm up")
        else:
            print('he he he')
            self.__robot_controller.right_arm(True)
            sleep(0.05)

    def right_arm_down(self) -> None:
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"right arm down")
        else:
            self.__robot_controller.right_arm(False)
            sleep(0.05)

    def head_left(self) -> None:
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"head left")
        else:
            self.__robot_controller.head_shake(False)
            sleep(0.05)

    def head_right(self) -> None:
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"head right")
        else:
            self.__robot_controller.head_shake(True)
            sleep(0.05)

    def head_up(self) -> None:
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"head up")
        else:
            self.__robot_controller.head_nod(True)
            sleep(0.05)

    def head_down(self) -> None:
        if self.__platform == "Windows" or self.__platform == "Darwin":
            print(f"head down")
        else:
            self.__robot_controller.head_shake(False)
            sleep(0.05)


if __name__ == "__main__":
    rc: ControllerInterface = ControllerInterface()
