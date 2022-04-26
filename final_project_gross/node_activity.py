from abc import ABC, abstractmethod

from player_statistics import PlayerStatistics


class NodeActivity(ABC):
    """
    This class acts as an interface for node activities.
    """

    def __init__(self, player_statistics: PlayerStatistics) -> None:
        self.type = self.__class__.__name__
        self.player_statistics: PlayerStatistics = player_statistics

    @abstractmethod
    def node_activity(self) -> None:
        """
        Handles the activity that occurs at this Node.
        :return: None.
        """
        pass
