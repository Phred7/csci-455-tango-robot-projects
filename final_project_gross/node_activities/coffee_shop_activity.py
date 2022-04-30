import os
from typing import Tuple

import player_statistics
from controller_interface import ControllerInterface
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech


class CoffeeShopActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        super().__init__(player_statistics)
        self.end_x = None
        self.end_y = None

    def node_activity(self) -> None:
        # updates kivy graphics
        curX = self.player_statistics.current_x
        curY = self.player_statistics.current_y
        with open('images/picture.txt', "w") as f:
            f.write('images/coffee-shop.jpeg')
        if self.end_x == None or self.end_y == None:
            print("coffee shop closed due to covid :(")
        else:
            calc_x = curX - self.end_x
            calc_y = curY - self.end_y

            if abs(calc_x) > abs(calc_y) :
                if calc_x > 0:
                    Speech.say("exit is to the west")
                else:
                    Speech.say("exit is to the east")
            else:
                if calc_y > 0:
                    Speech.say("exit is to the north")
                else:
                    Speech.say("exit is to the south")



        # depending on how node layout is we could either just have some value range determine a direction
        # or we can just figure something else out. This does nothing for now though

    def set_end_coordinates(self, coordinates: Tuple[int, int]) -> None:
        self.end_x, self.end_y = coordinates
        