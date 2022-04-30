from controller_interface import ControllerInterface
from node_activity import NodeActivity
from player_statistics import PlayerStatistics

from speech import Speech


class EndActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        NodeActivity.__init__(self, player_statistics, controller_interface)

    def node_activity(self) -> None:
        # updates kivy graphics
        with open('images/picture.txt', "w") as f:
            f.write('images/finish.jpeg')
        Speech().say('You won!')
        self.controller_interface.left_arm_up()
        self.controller_interface.left_arm_down()
        self.controller_interface.right_arm_up()
        self.controller_interface.right_arm_down()
        self.controller_interface.left_arm_up()
        self.controller_interface.left_arm_down()
        self.controller_interface.right_arm_up()
        self.controller_interface.right_arm_down()