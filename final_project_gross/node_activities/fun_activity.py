import random

from controller_interface import ControllerInterface
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech

class FunActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        super().__init__(player_statistics)

    def node_activity(self) -> None:
        # updates kivy graphics
        with open('images/picture.txt', "w") as f:
            f.write('images/fun.png')

        fun_choices = ['die', 'heal', 'armor', 'nothing', 'lore']
        choice = random.choice(fun_choices)

        if choice == 'die':
            self.player_statistics.set_health(0)
            Speech.say('you\'re dead roll better next time')
            # TODO: do exit stuff here... this should be handled by the game_runner
        elif choice == 'heal':
            self.player_statistics.set_health(400)
            Speech.say('healed health')
        elif choice == 'armor':
            self.player_statistics.modify_armour_class(self.player_statistics.armour_class()+1)
            Speech.say('armor armored')
        elif choice == 'lore':
            Speech.say('lore placeholder')
            # TODO: read a lore document. Not sure if TTS can just do file inputs
        else:
            Speech.say('nothing happened.\nL')
