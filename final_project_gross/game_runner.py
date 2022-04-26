from speech import Speech
import random as rand
from typing import Tuple

from player_statistics import PlayerStatistics


class IdRatherRipMyNailOFF:

    def __init__(self) -> None:
        self.this_is_the_players_stats_they_gonna_die_lol: PlayerStatistics = PlayerStatistics(
            player_name="Steven the Slow to Die")
        self.current_coordinates = self.initial_coordinates()
        self.next_coordinates = (0, 0)
        self.end_coordinates = self.calc_end_coordinates()
        self.total_moves = 0
        self.map = [['x', 1, 'x', 1, 'x', 0, 'x', 1, 'x'],
                    [  0,  0,  1,  0,  1,  0,  0,  0,  1],
                    ['x', 1, 'x', 0, 'x', 0, 'x', 1, 'x'],
                    [  1,  0,  1,  0,  0,  0,  1,  0,  1],
                    ['x', 0, 'x', 1, 'x', 1, 'x', 0, 'x'],
                    [  1,  0,  0,  0,  0,  0,  1,  0,  1],
                    ['x', 1, 'x', 0, 'x', 0, 'x', 1, 'x'],
                    [  0,  0,  1,  0,  1,  0,  1,  0,  0],
                    ['x', 1, 'x', 1, 'x', 0, 'x', 1, 'x']]
        self.direction_facing = 'north'  # Completly arbitrary, since we dont have sensor, will either be north south west or east
        self.lesser_y = {'north': None, 'east': 'left90', 'south': '180', 'west': 'right90'}
        self.greater_y = {'north': '180', 'east': 'right90', 'south': None, 'west': 'left90'}
        self.lesser_x = {'north': 'left90', 'east': '180', 'south': 'right90', 'west': None}
        self.greater_x = {'north': 'right90', 'east': None, 'south': 'left90', 'west': '180'}

    @staticmethod
    def initial_coordinates(self) -> Tuple[int, int]:
        '''
        given the map of the maze find all possible starting points along the edges, and return a random one
        :return: starting coordinate (x,y)
        '''
        possible_start_coords = []
        # find all the possible start coordinates along the top and bottom edge of map
        for i in range(0, len(self.map[0])):
            if self.map[i][0] == 'x':
                possible_start_coords.append((i, 0))
            if self.map[i][len(self.map) - 1] == 'x':
                possible_start_coords.append((i, (len(self.map) - 1)))
        # find all the possible start coordinates along the left and right edge of map
        for i in range(0, len(self.map)):
            if self.map[0][i] == 'x':
                possible_start_coords.append((0, i))
            if self.map[len(self.map[0] - 1)][i] == 'x':
                possible_start_coords.append((len(self.map[0] - 1), i))
        # return a random possible start coordinate
        return rand.choice(possible_start_coords)

    @staticmethod
    def calc_end_coordinates(self) -> Tuple[int, int]:
        '''
        takes the initial coordinates and calculates and end coordinate on the opposite edge of the map
        :return: end coordinates
        '''
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
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'x':
                    #TODO set x to a random node
                    pass

    def userInput(self):
        '''
        Calculates possible directions the robot can move based on current coordinates
        Asks user what desired direction is
        :return: coordinates robot should move to
        '''
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

    def move(self, new_coords):
        if new_coords == self.end_coordinates:
            print('you made it to the finish, end of the line pal')
            #TODO update game lodgic acordingly
        x = self.current_coordinates[0]
        y = self.current_coordinates[1]
        new_x = new_coords[0]
        new_y = new_coords[1]

        if self.total_moves < 30:
            if new_y < y:
                self.lesser_y[self.direction_facing]  # TODO modify dict so value calls turn function
                self.movefwd  # TODO actually call fwd
                self.direction_facing = 'north'
            if new_y > y:
                self.greater_y[self.direction_facing]
                self.movefwd  # TODO actually call fwd
                self.direction_facing = 'south'
            if new_x < x:
                self.lesser_x[self.direction_facing]
                self.movefwd  # TODO actually call fwd
                self.direction_facing = 'west'
            if new_x > x:
                self.greater_x[self.direction_facing]
                self.movefwd  # TODO actually call fwd
                self.direction_facing = 'east'
            self.total_moves += 1
        else:
            print('You moved too many times, ur done')
            # TODO affect robot stats

    """
    NOTE: Yes, everything was moved... it wasn't deleted. See /node_activities/...
    """

    def on_finish(self):  # TODO: note we don't need the key for this to work
        print('you finished')
