from random import random
from typing import Tuple

from player_statistics import PlayerStatistics


class IdRatherRipMyNailOFF:

    def __init__(self) -> None:
        self.this_is_the_player_they_gonna_die_lol: PlayerStatistics = PlayerStatistics("Steven the Slow")
        self.current_coordinates = self.initial_coordinates()
        self.next_coordinates = (0, 0)

    @staticmethod
    def initial_coordinates() -> Tuple[int, int]:
        return 0, 0

    """
    NOTE: Yes, everything was moved... it wasn't deleted. See /node_activities/...
    """

    def on_finish(self):  # TODO: note we don't need the key for this to work
        print('you finished')
