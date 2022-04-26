from node_activity import NodeActivity
from player_statistics import PlayerStatistics


class CoffeeShopActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics) -> None:
        super().__init__(player_statistics)

    def node_activity(self) -> None:
        pass

    def signal_station(self):
        pass
        # depending on how node layout is we could either just have some value range determine a direction
        # or we can just figure something else out. This does nothing for now though
