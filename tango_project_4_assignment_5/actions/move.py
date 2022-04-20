from tango_project_4_assignment_5.action_stategy import ActionStrategy


class Move(ActionStrategy):

    def __init__(self, move_forward_bool: bool, distance_to_move: int) -> None:
        super().__init__()
        self.move_forward_bool: bool = move_forward_bool
        self.distance_to_move: int = distance_to_move

    def execute_action(self) -> None:
        return