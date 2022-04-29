from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech


class StartActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics) -> None:
        NodeActivity.__init__(self, player_statistics)

    def node_activity(self) -> None:
        # updates kivy graphics
        with open('images/picture.txt', "w") as f:
            f.write('images/start.png')
        Speech.say("Robot starting")
        pass
