import os
import platform
import sys
import threading
from copy import deepcopy

from kivy_screen import BackgroundApp
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
        # keeps track of location, and total moves level
        self.current_coordinates = self.initial_coordinates()
        # self.next_coordinates = (0, 0)
        self.end_coordinates = self.calc_end_coordinates()

        for node in self.node_array:
            if isinstance(node.node_activity, CoffeeShopActivity):
                node.node_activity.set_end_coordinates(self.end_coordinates)

        # must happen after end and current
        self.populate_map()

        self.total_moves = 0
        # Used to move robot in correct directions
        self.direction_facing = 'north'  # Completely arbitrary but we need it
        # 1 second is for 90 degrees, 2 is for 180, can change later if needed

        self.visited_coordinates: List[Tuple[int, int]] = [self.current_coordinates]

        self.lesser_y: Dict[str, (Callable, int)] = {'east': (self.robot_controller_interface.turn_left, 2),
                                                     'south': (self.robot_controller_interface.turn_left, 4),
                                                     'west': (self.robot_controller_interface.turn_right, 2)}
        self.greater_y: Dict[str, (Callable, int)] = {'north': (self.robot_controller_interface.turn_left, 4),
                                                      'east': (self.robot_controller_interface.turn_right, 2),
                                                      'west': (self.robot_controller_interface.turn_left, 2)}
        self.lesser_x: Dict[str, (Callable, int)] = {'north': (self.robot_controller_interface.turn_left, 2),
                                                     'east': (self.robot_controller_interface.turn_left, 4),
                                                     'south': (self.robot_controller_interface.turn_right, 2)}
        self.greater_x: Dict[str, (Callable, int)] = {'north': (self.robot_controller_interface.turn_right, 2),
                                                      'south': (self.robot_controller_interface.turn_left, 2),
                                                      'west': (self.robot_controller_interface.turn_left, 4)}

        with open('images/picture.txt', "w") as f:
            f.write("images/gray.jpg")

        self.gui_thread: threading.Thread = threading.Thread(name="gui thread", target=self.gui, args=())
        self.gui_thread.start()

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
        sc = rand.choice(possible_start_coordinates)
        self.map[sc[0]][sc[1]] = Node("Start", StartActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                             self.robot_controller_interface))
        # return a random possible start coordinate
        return sc

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
        self.map[coords[0]][coords[1]] = Node("End", EndActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                                 self.robot_controller_interface))
        return coords

    def populate_map(self):
        """
        swaps x's in the map for nodes, randomly populates the map
        :return: None
        """
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'x':
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
        print(self.map_as_a_string())
        for k in range(len(row)):
            try:
                if (x + row[k]) < 0 or (x + row[k]) > (len(self.map[0]) - 1):
                    continue
                if (y + col[k]) < 0 or (y + col[k]) > (len(self.map) - 1):
                    continue
                if self.map[x + row[k]][y + col[k]] != 0:
                    possible_moves[direction[k]] = (x + row[k], y + col[k])
            except IndexError:
                print('index error')
                pass

        output = 'Please select a direction ' + str(possible_moves.keys())
        print(output)
        Speech.say(output)
        user_choice = ''
        im_crying_real_tears: List[str] = ['north', 'south', 'west', 'east']
        while True:
            user_choice = Speech.get_speech().lower()
            for x in im_crying_real_tears:
                if x in user_choice and x in possible_moves:
                    return possible_moves[x]

    def move(self, new_coordinate: Tuple[int, int]):
        x, y = self.current_coordinates
        new_x, new_y = new_coordinate
        with open('images/picture.txt', "w") as f:
            f.write('images/traveling.png')

        if self.total_moves < 30 and self.this_is_the_players_stats_they_gonna_die_lol.health() > 0:
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
            self.robot_controller_interface.forward(1)
            self.current_coordinates = new_coordinate
            self.this_is_the_players_stats_they_gonna_die_lol.update_current_position(self.current_coordinates)
            if self.current_coordinates not in self.visited_coordinates:
                self.visited_coordinates.append(self.current_coordinates)
            self.act_out_node(new_coordinate)
            if self.current_coordinates not in self.visited_coordinates:
                self.visited_coordinates.append(self.current_coordinates)

        else:
            Speech.say('You moved too many times, ur dead')
            self.this_is_the_players_stats_they_gonna_die_lol.set_health(0)
            with open('images/picture.txt', "w") as f:
                f.write('images/dead.png')
            self.on_finish()
            # TODO affect robot stats, do something, kill robot or hunter?

        # print(self.map_as_a_string())

    def act_out_node(self, coordinates: Tuple[int, int]):
        this_item: Any = self.map[coordinates[0]][coordinates[1]]
        if not isinstance(this_item, int):
            if isinstance(this_item, Node):
                this_item.execute_node_activity()
                if isinstance(this_item.node_activity,
                              EndActivity) or self.this_is_the_players_stats_they_gonna_die_lol.health() < 1:
                    self.on_finish()
                    return
            else:
                print("Not a Node")

    def flee(self):
        x_coordinate: int = rand.randint(0, (len(self.map[0]) - 1))
        y_coordinate: int = rand.randint(0, (len(self.map) - 1))
        random_node = self.map[x_coordinate][y_coordinate]
        print(random_node)
        while random_node == self.current_coordinates or random_node == self.end_coordinates or random_node == '0' or random_node == '1':
            x_coordinate: int = rand.randint(0, (len(self.map[0]) - 1))
            y_coordinate: int = rand.randint(0, (len(self.map) - 1))
            random_node = self.map[x_coordinate][y_coordinate]
            print(random_node)
        self.robot_controller_interface.turn_right(5)
        Speech.say("You have been moved to a random node.")
        # print(self.map_as_a_string())
        self.current_coordinates = (x_coordinate, y_coordinate)
        if self.current_coordinates not in self.visited_coordinates:
            self.visited_coordinates.append(self.current_coordinates)
        self.this_is_the_players_stats_they_gonna_die_lol.update_current_position(self.current_coordinates)
        self.this_is_the_players_stats_they_gonna_die_lol.update_fleeing(False)
        print(self.this_is_the_players_stats_they_gonna_die_lol.get_fleeing())

    def generate_nodes(self) -> List[Node]:
        return [Node("Easy Fight 0", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Easy Fight 1", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Easy Fight 2", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Easy Fight 3", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Easy Fight 4", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Easy Fight 5", EasyBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Medium Fight 0", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                            self.robot_controller_interface)),
                Node("Medium Fight 1", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                            self.robot_controller_interface)),
                Node("Medium Fight 2", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                            self.robot_controller_interface)),
                Node("Medium Fight 3", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                            self.robot_controller_interface)),
                Node("Medium Fight 4", MediumBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                            self.robot_controller_interface)),
                Node("Hard Fight 0", HardBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Hard Fight 1", HardBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Hard Fight 2", HardBattleActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                        self.robot_controller_interface)),
                Node("Charging Station 0", ChargingStationActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                                   self.robot_controller_interface)),
                Node("Charging Station 1", ChargingStationActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                                   self.robot_controller_interface)),
                Node("Charging Station 2", ChargingStationActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                                   self.robot_controller_interface)),
                Node("Coffee Shop 0", CoffeeShopActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                         self.robot_controller_interface)),
                Node("Coffee Shop 1", CoffeeShopActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                         self.robot_controller_interface)),
                Node("Fun 0", FunActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                          self.robot_controller_interface)),
                Node("Fun 1", FunActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                          self.robot_controller_interface)),
                Node("Fun 2", FunActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                          self.robot_controller_interface)),
                Node("Puzzle 0", TrickyChoiceTypeActivity(self.this_is_the_players_stats_they_gonna_die_lol,
                                                          self.robot_controller_interface))]

    def on_finish(self):  # TODO: note we don't need the key for this to work
        print('you finished')
        if self.this_is_the_players_stats_they_gonna_die_lol.health() > 0:
            Speech.say("You completed the maze. Im dead now.")
        else:
            Speech.say("You died. You are a loser, you lost.")
        if platform.system() != "Darwin":
            self.gui_thread.join(1)
        sys.exit(0)

    def gui(self) -> None:
        BackgroundApp().run()

    # Connie
    # TODO: when going WEST and NORTH only you can wrap around to the nodes on the other side (Like pacman). Is that intentional?

    # Justin
    # todo make robot move while it is fighting battles (arms turning etc) - all other actions are done
    # i want to check in on how best to do this (ie. class and steps etc)
    # t\odo after each fight round tell user how robot and bad buys are doing - ie "I have 16 hit points left, the bad guys have 12"
    # t\odo if we run away number of bad guys should be maintained - ie we defeat 3 of 5, when we return 2 are left
    # t\odo allow users to run or stay during fight

    # Whoever
    # todo - address any other misc todos around the code
    # t/odo - check flee works
    # todo - make end game logic - if we die and when we finish what happens
    # t/odo - finish battle game logic
    # todo - check that robot moves during node action execution

    def map_as_a_string(self) -> str:
        return_string: str = ""
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if (x, y) == self.current_coordinates:
                    return_string += "X"
                elif (x, y) in self.visited_coordinates:
                    item = self.map[x][y]
                    if isinstance(item, Node):
                        return_string += "1"
                    if isinstance(item, int):
                        return_string += str(item)
                else:
                    return_string += "0"
            return_string += "\n"
        return return_string

    def __str__(self) -> str:
        return self.map_as_a_string()


# TODO: this is just a note... the STOP function may be causing the robot's weird movements after inactivity.
if __name__ == '__main__':
    driver = IdRatherRipMyNailOFF()
    driver.act_out_node(driver.current_coordinates)
    try:
        while True:
            if not driver.this_is_the_players_stats_they_gonna_die_lol.get_fleeing():
                new_coordinates = driver.user_input()
                driver.move(new_coordinates)
            else:
                driver.flee()
                driver.this_is_the_players_stats_they_gonna_die_lol.update_fleeing(False)
    finally:
        driver.gui_thread.join()
