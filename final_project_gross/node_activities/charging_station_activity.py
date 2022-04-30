from controller_interface import ControllerInterface
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech

class ChargingStationActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        super().__init__(player_statistics, controller_interface)

    def node_activity(self) -> None:
        with open('images/picture.txt', "w") as f:
            f.write('images/charging-station.png')

        self.player_statistics.set_health(400)  # TODO: should it recharge a random amount of health in a range that doesnt exceed some ceiling.

        self.controller_interface.turn_left(1)
        self.controller_interface.turn_right(1)
        Speech.say('recharged health i guess')

