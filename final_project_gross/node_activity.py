from abc import ABC, abstractmethod


class NodeActivity(ABC):
    """
    This class acts as an interface for node activities.
    """

    def __init__(self) -> None:
        self.type = self.__class__.__name__

    @abstractmethod
    def node_activity(self) -> None:
        """
        Handles the activity that occurs at this Node.
        :return: None.
        """
        pass

