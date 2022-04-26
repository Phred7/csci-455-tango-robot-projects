from node_activities.battle import Battle, BattleDifficulty
from node_activity import NodeActivity
from player_statistics import PlayerStatistics


class MediumBattleActivity(NodeActivity, Battle):

    def __init__(self, player_statistics: PlayerStatistics) -> None:
        NodeActivity.__init__(self, player_statistics)
        Battle.__init__(self, BattleDifficulty.MEDIUM, self.player_statistics)

    def node_activity(self) -> None:
        pass
