from time import sleep

from controller_interface import ControllerInterface
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech


class StartActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        NodeActivity.__init__(self, player_statistics, controller_interface)

    def node_activity(self) -> None:
        # updates kivy graphics
        print('called right arm up')
        self.controller_interface.right_arm_up()
        print('just called it')
        sleep(1)
        self.controller_interface.left_arm_up()
        sleep(1)
        Speech.say("Robot starting")
        Speech.say('Navigate the maze, defeat enemies and make it to the end to win!')
        sleep(1)
        self.controller_interface.right_arm_down()
        sleep(1)
        self.controller_interface.left_arm_down()
        sleep(1)
