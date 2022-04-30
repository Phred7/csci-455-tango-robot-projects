from node_activities.charging_station_activity import ChargingStationActivity
from node_activities.coffee_shop_activity import CoffeeShopActivity
from node_activities.easy_battle_activity import EasyBattleActivity
from node_activities.end_activity import EndActivity
from node_activities.fun_activity import FunActivity
from node_activities.hard_battle_activity import HardBattleActivity
from node_activities.medium_battle_activity import MediumBattleActivity
from node_activities.start_activity import StartActivity
from node_activities.tricky_choice_type_activity import TrickyChoiceTypeActivity
from speech import Speech
from player_statistics import PlayerStatistics
from controller_interface import ControllerInterface
from typing import Tuple, List, Any, Callable, Dict
from node import Node
import random as rand


class IdRatherRipMyNailOFF:

    def __init__(self) -> None:
        self.this_is_the_players_stats_they_gonna_die_lol: PlayerStatistics = PlayerStatistics(
            player_name="Steven the Slow to Die")

        self.robot_controller_interface: ControllerInterface = ControllerInterface()

        # x = placeholder for node, 1 = connecting path between nodes, 0 = no path
        self.map = [['x', 1, 'x', 1, 'x', 0, 'x', 1, 'x'],
                    [0, 0, 1, 0, 1, 0, 0, 0, 1],
                    ['x', 1, 'x', 0, 'x', 0, 'x', 1, 'x'],
                    [1, 0, 1, 0, 0, 0, 1, 0, 1],
                    ['x', 0, 'x', 1, 'x', 1, 'x', 0, 'x'],
                    [1, 0, 0, 0, 0, 0, 1, 0, 1],
                    ['x', 1, 'x', 0, 'x', 0, 'x', 1, 'x'],
                    [0, 0, 1, 0, 1, 0, 1, 0, 0],
                    ['x', 1, 'x', 1, 'x', 0, 'x', 1, 'x']]
        self.node_array = self.generate_nodes()

        # keeps track of location, and total moves levt
        self.current_coordinates = self.initial_coordinates()
        # self.next_coordinates = (0, 0)
        self.node_coordinates = []
        self.end_coordinates = self.calc_end_coordinates()
        self.total_moves = 0
        self.map: List[List[Any]] = [['x', 1, 'x', 1, 'x', 0, 'x', 1, 'x'],
                                     [0, 0, 1, 0, 1, 0, 0, 0, 1],
                                     ['x', 1, 'x', 0, 'x', 0, 'x', 1, 'x'],
                                     [1, 0, 1, 0, 0, 0, 1, 0, 1],
                                     ['x', 0, 'x', 1, 'x', 1, 'x', 0, 'x'],
                                     [1, 0, 0, 0, 0, 0, 1, 0, 1],
                                     ['x', 1, 'x', 0, 'x', 0, 'x', 1, 'x'],
                                     [0, 0, 1, 0, 1, 0, 1, 0, 0],
                                     ['x', 1, 'x', 1, 'x', 0, 'x', 1, 'x']]
        self.node_array = self.generate_nodes()

        # Used to move robot in correct directions
        self.direction_facing = 'north'  # Completely arbitrary but we need it
        # 1 second is for 90 degrees, 2 is for 180, can change later if needed

        self.lesser_y: Dict[str, (Callable, int)] = {'east': (self.robot_controller_interface.turn_left, 1),
                                                     'south': (self.robot_controller_interface.turn_left, 2),
                                                     'west': (self.robot_controller_interface.turn_right, 1)}
        self.greater_y: Dict[str, (Callable, int)] = {'north': (self.robot_controller_interface.turn_left, 2),
                                                      'east': (self.robot_controller_interface.turn_right, 1),
                                                      'west': (self.robot_controller_interface.turn_left, 1)}
        self.lesser_x: Dict[str, (Callable, int)] = {'north': (self.robot_controller_interface.turn_left, 1),
                                                     'east': (self.robot_controller_interface.turn_left, 2),
                                                     'south': (self.robot_controller_interface.turn_right, 1)}
        self.greater_x: Dict[str, (Callable, int)] = {'north': (self.robot_controller_interface.turn_right, 1),
                                                      'south': (self.robot_controller_interface.turn_left, 1),
                                                      'west': (self.robot_controller_interface.turn_left, 2)}

    def initial_coordinates(self) -> Tuple[int, int]:
        """
        given the map of the maze find all possible starting points along the edges, and return a random one
        :return: starting coordinate (x,y)
        """
        possible_start_coordinates = []
        # find all the possible start coordinates along the top and bottom edge of map
        for i in range(0, len(self.map[0])):
            if self.map[i][0] == 'x':
                possible_start_coordinates.append((i, 0))
            if self.map[i][len(self.map) - 1] == 'x':
                possible_start_coordinates.append((i, (len(self.map) - 1)))
        # find all the possible start coordinates along the left and right edge of map
        for i in range(0, len(self.map)):
            if self.map[0][i] == 'x':
                possible_start_coordinates.append((0, i))
            if self.map[len(self.map[0]) - 1][i] == 'x':
                possible_start_coordinates.append((len(self.map[0]) - 1, i))
        # return a random possible start coordinate
        return rand.choice(possible_start_coordinates)

    def calc_end_coordinates(self) -> Tuple[int, int]:
        """
        takes the initial coordinates and calculates and end coordinate on the opposite edge of the map
        :return: end coordinates
        """
        possible_y = []
        if self.current_coordinates[0] == 0:
            x = len(self.map[0]) - 1
        else:
            x = 0
        for i in range(len(self.map)):
            if self.map[x][i] == 'x':
                possible_y.append(i)

        coords = (x, rand.choice(possible_y))
        return coords

    def populate_map(self):
        """
        swaps x's in the map for nodes, randomly populates the map
        :return: None
        """
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'x':
                    self.node_coordinates.append((i, j))
                    node = rand.choice(self.node_array)
                    while node.placed_in_map:
                        node = rand.choice(self.node_array)
                    self.map[i][j] = node
                    node.placed_in_map = True

    def user_input(self):
        """
        Calculates possible directions the robot can move based on current coordinates
        Asks user what desired direction is
        :return: coordinates robot should move to
        """
        possible_moves = {}
        x = self.current_coordinates[0]
        y = self.current_coordinates[1]
        row = [-1, 0, 0, 1]
        col = [0, -1, 1, 0]
        direction = ['north', 'west', 'east', 'south']
        for k in range(len(row)):
            try:
                if self.map[x + row[k]][y + col[k]] != 0:
                    possible_moves[direction[k]] = (x + row[k], y + col[k])
            except IndexError:
                pass

        output = 'Please select a direction ' + str(possible_moves.keys())
        Speech().say(output)
        user_choice = ''
        while user_choice not in possible_moves:
            user_choice = Speech().get_speech()

        return possible_moves[user_choice]

    def move(self, new_coords: Tuple[int, int]):
        x, y = self.current_coordinates
        new_x, new_y = new_coords

        if self.total_moves < 30:
            if new_y < y:
                if self.direction_facing in self.lesser_y:
                    function, time = self.lesser_y[self.direction_facing]
                    function(time)
                    self.direction_facing = 'north'
            if new_y > y:
                if self.direction_facing in self.greater_y:
                    function, time = self.greater_y[self.direction_facing]
                    function(time)
                self.direction_facing = 'south'
            if new_x < x:
                if self.direction_facing in self.lesser_x:
                    function, time = self.lesser_x[self.direction_facing]
                    function(time)
                self.direction_facing = 'west'
            if new_x > x:
                if self.direction_facing in self.greater_x:
                    function, time = self.greater_x[self.direction_facing]
                    function(time)
                self.direction_facing = 'east'
            self.total_moves += 1
            self.robot_controller_interface.forward(2)
            self.act_out_node(new_coords)
            self.current_coordinates = new_coordinates
        else:
            print('You moved too many times, ur done')
            # TODO affect robot stats, do something, kill robot or hunter?

    def act_out_node(self, coordinates: Tuple[int, int]):
        if self.map[coordinates[0]][coordinates[1]] == '1':
            pass
        if self.map[coordinates[0]][coordinates[1]] == '0':
            print('we are off the map, this is bad')
        else:
            self.map[coordinates[0]][coordinates[1]].execute_node_activity()

    def flee(self):
        random_node = rand.choice(self.node_coordinates)
        while random_node == self.current_coordinates or random_node == self.end_coordinates:
            random_node = rand.choice(self.node_coordinates)
        Speech.say("You have been moved to a random node.")
        self.current_coordinates = random_node

        # Connie
        # t\odo set up driver - call node actions everytime we are at a node
        # t\odo if users run from fight send to a random node, dont activate node, ask user where to move next
        # Justin
        # t\odo allow users to run or stay during fight
        # todo after each fight round tell user how robot and bad buys are doing - ie "I have 16 hit points left, the bad guys have 12"
        # t\odo if we run away number of bad guys should be mantained - ie we defeat 3 of 5, when we return 2 are left
        # Walker
        # todo threading for gui
        # t\odo set up arm functionality in controller interface
        # Whoever
        # todo address any other misc todos around the code
        # todo robots move during actions (arms turning etc)

    def generate_nodes(self) -> List[Node]:
        return [Node("Start", StartActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                            self.robot_controller_interface)),
                Node("End", EndActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Easy Fight 0", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Easy Fight 1", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Easy Fight 2", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Easy Fight 3", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Easy Fight 4", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Easy Fight 5", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Medium Fight 0", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Medium Fight 1", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Medium Fight 2", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Medium Fight 3", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Medium Fight 4", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Hard Fight 0", HardBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Hard Fight 1", HardBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Hard Fight 2", HardBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Charging Station 0", ChargingStationActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Charging Station 1", ChargingStationActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Charging Station 2", ChargingStationActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Coffee Shop 0", CoffeeShopActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Coffee Shop 1", CoffeeShopActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Fun 0", FunActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Fun 1", FunActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Fun 2", FunActivity(self.this_is_the_players_stats_they_gonna_die_lol)),
                Node("Puzzle 0", TrickyChoiceTypeActivity(self.this_is_the_players_stats_they_gonna_die_lol))]

    def on_finish(self):  # TODO: note we don't need the key for this to work
        print('you finished')


# TODO: this is just a note... the STOP function may be causing the robot's weird movements after inactivity.
if __name__ == '__main__':
    driver = IdRatherRipMyNailOFF()
    while True:
        if not driver.this_is_the_players_stats_they_gonna_die_lol.fleeing:
            new_coordinates = driver.user_input()
            driver.move(new_coordinates)
        else:
            driver.flee()
            driver.this_is_the_players_stats_they_gonna_die_lol.fleeing = False
