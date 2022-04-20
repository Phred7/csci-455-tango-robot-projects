from tango_project_4_assignment_5.action_stategy import ActionStrategy


class Turn(ActionStrategy):

    def __init__(self, turn_left_bool: bool, turn_angle: int) -> None:
        super().__init__()
        self.turn_left_bool: bool = turn_left_bool
        self.turn_angle: int = turn_angle

    def execute_action(self) -> None:
        return