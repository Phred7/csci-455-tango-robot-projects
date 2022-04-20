from abc import ABC, abstractmethod


class ActionStrategy(ABC):
    """
    This class acts as an interface for action.
    """

    def __init__(self) -> None:
        self.type = self.__class__.__name__

    @abstractmethod
    def execute_action(self) -> None:
        """
        Executes the action defined by this action.
        :return: None.
        """
        pass


