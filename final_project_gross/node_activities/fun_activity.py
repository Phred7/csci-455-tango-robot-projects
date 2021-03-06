import random

from controller_interface import ControllerInterface
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech

class FunActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        super().__init__(player_statistics, controller_interface)

    def node_activity(self) -> None:
        # updates kivy graphics
        with open('images/picture.txt', "w") as f:
            f.write('images/fun.png')

        fun_choices = ['die', 'heal', 'armor', 'nothing', 'lore']
        choice = random.choice(fun_choices)

        if choice == 'die':
            self.player_statistics.set_health(0)
            Speech.say('you\'re dead roll better next time')
            # TODO: do exit stuff here... this should be handled by the game_runner and make robot move
        elif choice == 'heal':
            self.player_statistics.set_health(self.player_statistics.health()+400)
            Speech.say('healed health')
            self.controller_interface.right_arm_up()
            sleep(1)
            self.controller_interface.right_arm_down()
            sleep(1)
        elif choice == 'armor':
            self.player_statistics.modify_armour_class(self.player_statistics.armour_class()+100)
            self.controller_interface.right_arm_up()
            sleep(1)
            Speech.say('armor armored')
            sleep(1)
            self.controller_interface.right_arm_down()
            sleep(1)
        elif choice == 'lore':
            self.controller_interface.right_arm_up()
            sleep(1)
            Speech.say('One ring to rule them all, one ring to find them, One ring to bring them all, and in the darkness bind them; In the Land of Mordor where the shadows lie.')
            sleep(1)
            self.controller_interface.right_arm_down()
            sleep(1)
        else:
            Speech.say('nothing happened.\nL')
