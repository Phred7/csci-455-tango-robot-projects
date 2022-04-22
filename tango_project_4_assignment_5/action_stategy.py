from abc import ABC, abstractmethod

from controller import Controller


class ActionStrategy(ABC):
    """
    This class acts as an interface for action.
    """

    def __init__(self) -> None:
        self.type = self.__class__.__name__

    @abstractmethod
    def execute_action(self, controller: Controller) -> None:
        """
        Executes the action defined by this action.
        :return: None.
        """
        pass


