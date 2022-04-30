from controller_interface import ControllerInterface
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech


class StartActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        NodeActivity.__init__(self, player_statistics, controller_interface)

    def node_activity(self) -> None:
        # updates kivy graphics
        with open('images/picture.txt', "w") as f:
            f.write('images/start.png')
        Speech.say("Robot starting")
        Speech.say('Navigate the maze, defeat enemies and make it to the end to win!')
