from node_activity import NodeActivity
from player_statistics import PlayerStatistics


class ChargingStationActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics) -> None:
        super().__init__(player_statistics)

    def node_activity(self) -> None:
        self.player_statistics.set_health(400)  # TODO: should it recharge a random amount of health in a range that doesnt exceed some ceiling.
        print('recharged health i guess')
