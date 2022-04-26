import random

from node_activity import NodeActivity
from player_statistics import PlayerStatistics


class FunActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics) -> None:
        super().__init__(player_statistics)

    def node_activity(self) -> None:
        pass

    def fun_node(self):
        fun_choices = ['die', 'heal', 'armor', 'nothing', 'lore']
        choice = random.choice(fun_choices)

        if choice == 'die':
            self.player_statistics.set_health(0)
            print('you\'re dead roll better next time')
            # TODO: do exit stuff here... this should be handled by the game_runner
        elif choice == 'heal':
            self.player_statistics.set_health(400)
            print('healed health')
        elif choice == 'armor':
            self.player_statistics.modify_armour_class(self.player_statistics.armour_class()+1)
            print('armor armored')
        elif choice == 'lore':
            print('lore placeholder')
            # TODO: read a lore document. Not sure if TTS can just do file inputs
        else:
            print('nothing happened.\nL')
