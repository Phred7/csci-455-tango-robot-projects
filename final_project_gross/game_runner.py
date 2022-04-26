from speech import Speech
from random import random
from typing import Tuple

from player_statistics import PlayerStatistics


class IdRatherRipMyNailOFF:

    def __init__(self) -> None:
        self.this_is_the_players_stats_they_gonna_die_lol: PlayerStatistics = PlayerStatistics(player_name="Steven the Slow to Die")
        self.current_coordinates = self.initial_coordinates()
        self.next_coordinates = (0, 0)

    @staticmethod
    def initial_coordinates() -> Tuple[int, int]:
        return 0, 0

    def initial_coords(self):
        return (0,0)


    def userInput(self):
        possible_moves = {}
        x = self.currentCoords[0]
        y = self.currentCoords[1]
        #TODO need try catch for index out of bounds
        if self.map[x-1][y] != 0:
           possible_moves['North'] = (x-1, y)
        if self.map[x+1][y] != 0:
           possible_moves['South'] = (x+1, y)
        if self.map[x][y+1] != 0:
           possible_moves['East'] = (x, y+1)
        if self.map[x][y-1] != 0:
           possible_moves['West'] = (x, y-1)

        output = 'Please select a direction' + possible_moves.keys()

        Speech(False, possible_moves.keys())

        #
        #
        # path.pop(0)
        # self.ycoor += 1
        # while path:
        #     if len(path) == 0:
        #         return
        #     coordiates = path.pop(0)
        #     x = coordiates[0]
        #     y = coordiates[1]
        #     _x, _y = (self.xcoor, self.ycoor)
        #
        #     if self.ycoor < y and (self.projected_position[2] == 0 or self.projected_position[2] == 360):
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"forward ({_x},{_y}) -> ({x},{y}))")
        #         self.ycoor += 1
        #     elif self.ycoor > y and self.projected_position[2] == 180:
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"forward ({_x},{_y}) -> ({x},{y}))")
        #         self.ycoor -= 1
        #     elif self.xcoor < x and self.projected_position[2] == 270:
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"forward ({_x},{_y}) -> ({x},{y}))")
        #         self.xcoor += 1
        #     elif self.xcoor > x and self.projected_position[2] == 90:
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"forward ({_x},{_y}) -> ({x},{y}))")
        #         self.xcoor -= 1
        #     elif self.xcoor < x and (self.projected_position[2] == 0 or self.projected_position[2] == 360):
        #         self.turn_90_pid(left=False, delay=3)
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"right forward ({_x},{_y}) -> ({x},{y}))")
        #         self.xcoor += 1
        #     elif self.xcoor > x and self.projected_position[2] == 180:
        #         self.turn_90_pid(left=True, delay=3)
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"left forward ({_x},{_y}) -> ({x},{y}))")
        #         self.xcoor -= 1
        #     elif self.xcoor > x and (self.projected_position[2] == 0 or self.projected_position[2] == 360):
        #         self.turn_90_pid(left=True, delay=3)
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"left forward ({_x},{_y}) -> ({x},{y}))")
        #         self.xcoor -= 1
        #     elif self.xcoor < x and self.projected_position[2] == 180:
        #         self.turn_90_pid(left=True, delay=3)
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"right forward ({_x},{_y}) -> ({x},{y}))")
        #         self.xcoor += 1
        #     elif self.ycoor < y and self.projected_position[2] == 270:
        #         self.turn_90_pid(left=True, delay=3)
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"left forward ({_x},{_y}) -> ({x},{y}))")
        #         self.ycoor += 1
        #     elif self.ycoor < y and self.projected_position[2] == 90:
        #         self.turn_90_pid(left=False, delay=3)
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"right forward ({_x},{_y}) -> ({x},{y}))")
        #         self.ycoor += 1
        #     elif self.ycoor > y and self.projected_position[2] == 270:
        #         self.turn_90_pid(left=False, delay=3)
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"right forward ({_x},{_y}) -> ({x},{y}))")
        #         self.ycoor -= 1
        #     elif self.ycoor > y and self.projected_position[2] == 90:
        #         self.turn_90_pid(left=True, delay=3)
        #         if len(path) == 0:
        #             return
        #         self.forward(self.radian_in_one_grid_space, delay=3)
        #         print(f"left forward ({_x},{_y}) -> ({x},{y}))")
        #         self.ycoor += 1
        # return
    """
    NOTE: Yes, everything was moved... it wasn't deleted. See /node_activities/...
    """

    def on_finish(self):  # TODO: note we don't need the key for this to work
        print('you finished')
