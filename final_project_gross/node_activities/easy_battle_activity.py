from controller_interface import ControllerInterface
from node_activities.battle import Battle, BattleDifficulty
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech


class EasyBattleActivity(NodeActivity, Battle):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        NodeActivity.__init__(self, player_statistics, controller_interface)
        Battle.__init__(self, BattleDifficulty.EASY, player_statistics, controller_interface)

    def node_activity(self) -> None:
        # updates kivy graphics
        with open('images/picture.txt', "w") as f:
            f.write('images/easy.png')

        self.battle()
