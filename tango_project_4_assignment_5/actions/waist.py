import platform

from action_stategy import ActionStrategy
from controller import Controller


class Waist(ActionStrategy):
    """
    Implements turning of the waist for this system.
    """

    def __init__(self, waist_turn_left_bool: bool) -> None:
        super().__init__()
        self.waist_turn_left_bool: bool = waist_turn_left_bool

    def execute_action(self, controller: Controller) -> None:
        """
        Causes the robot to turn the waist left or right.
        :param controller: Controller object to control this system.
        :return: None.
        """
        if platform.system() == 'Windows':
            print(f"turning waist {'left' if self.waist_turn_left_bool else 'right'}")
        else:
            controller.turn_waist(not self.waist_turn_left_bool)
        return
