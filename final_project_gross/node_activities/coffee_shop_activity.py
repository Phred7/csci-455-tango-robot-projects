from typing import Tuple

from controller_interface import ControllerInterface
from node import Node
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech


class CoffeeShopActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        super().__init__(player_statistics, controller_interface)
        self.end_x: int
        self.end_y: int

    def node_activity(self) -> None:
        with open('images/picture.txt', "w") as f:
            f.write('images/coffee-shop.jpeg')

        current_x_coordinate, current_y_coordinate = self.player_statistics.current_position()

        if self.end_x is None or self.end_y is None:
            print("coffee shop closed due to covid :(")
        else:
            calc_x = current_x_coordinate - self.end_x
            calc_y = current_y_coordinate - self.end_y

            if abs(calc_x) > abs(calc_y):
                if calc_x > 0:
                    Speech.say("exit is to the west")
                    self.controller_interface.turn_right(2)
                else:
                    Speech.say("exit is to the east")
                    self.controller_interface.turn_right(2)
            else:
                if calc_y > 0:
                    Speech.say("exit is to the north")
                    self.controller_interface.turn_left(2)
                else:
                    Speech.say("exit is to the south")
                    self.controller_interface.turn_left(2)

        # depending on how node layout is we could either just have some value range determine a direction
        # or we can just figure something else out. This does nothing for now though

    def set_end_coordinates(self, coordinates: Tuple[int, int]) -> None:
        self.end_x, self.end_y = coordinates


if __name__ == "__main__":
    node = Node("Coffee Shop 0", CoffeeShopActivity(PlayerStatistics("this is the name"),
                                                    ControllerInterface(), (1, 1)))
    node.execute_node_activity()
