from tango_project_4_assignment_5.action_stategy import ActionStrategy


class Speech(ActionStrategy):

    def __init__(self, arg_1, arg_2, arg_n):
        super().__init__()
        self.arg_1 = arg_1
        self.arg_2 = arg_2
        self.arg_n = arg_n

    def execute_action(self) -> None:
        return
