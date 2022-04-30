from abc import ABC, abstractmethod

from controller_interface import ControllerInterface
from player_statistics import PlayerStatistics


class NodeActivity(ABC):
    """
    This class acts as an interface for node activities.
    """

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        self.node_type = self.__class__.__name__
        self.player_statistics: PlayerStatistics = player_statistics
        self.controller_interface: ControllerInterface = controller_interface

    @abstractmethod
    def node_activity(self) -> None:
        """
        Children define and handle the activity that occurs at this Node by implementing this method.
        :return: None.
        """
        pass
