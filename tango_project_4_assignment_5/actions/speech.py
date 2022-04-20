from functools import partial

from tango_project_4_assignment_5.action_stategy import ActionStrategy


class Speech(ActionStrategy):

    def __init__(self, input_bool: bool, speech_string: str, test_arg_n): # can pass function to add to multiprocessing queue as a arg. Then call w/ arg(string)
        super().__init__()
        self.input_bool: bool = input_bool
        self.speech_string: str = speech_string
        self.arg_n = test_arg_n

    def execute_action(self) -> None:
        return

    # def test_method(self, string: str) -> str:
    #     return string
    #
    # def test(self) -> None:
    #     self.arg_n = partial(self.test_method, "test_string")
    #     print(self.arg_n())


if __name__ == "__main__":
    speech: Speech = Speech(1, 2, 3)
    # speech.test()
