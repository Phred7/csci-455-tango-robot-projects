from node_activity import NodeActivity
from player_statistics import PlayerStatistics


class EndActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics) -> None:
        NodeActivity.__init__(self, player_statistics)

    def node_activity(self) -> None:
        pass
