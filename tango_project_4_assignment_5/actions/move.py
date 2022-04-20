from tango_project_4_assignment_5.action_stategy import ActionStrategy
from tango_project_4_assignment_5.controller import Controller


class Move(ActionStrategy):

    def __init__(self, move_forward_bool: bool, distance_to_move: int) -> None:
        super().__init__()
        self.move_forward_bool: bool = move_forward_bool
        self.distance_to_move: int = distance_to_move

    def execute_action(self, controller: Controller) -> None:
        if self.move_forward_bool:
            controller.forward(controller.fivestepsofPOWER[1])
        # handle wait based on dist. input.
        return