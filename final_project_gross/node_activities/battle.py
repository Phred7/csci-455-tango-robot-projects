import random
from enum import Enum

import player_statistics
from player_statistics import PlayerStatistics
from speech import Speech


class BattleDifficulty(Enum):
    """
    Conveniently stores easily comparable values for the difficulty rating of a Battle.
    """
    EASY = 0
    MEDIUM = 1
    HARD = 2


class Battle:
    """
    Encapsulates Battles.
    """

    def __init__(self, difficulty: BattleDifficulty, player_stats: PlayerStatistics) -> None:
        self.battle_difficulty: BattleDifficulty = difficulty
        self.__player_stats: PlayerStatistics = player_stats
        self.__enemy_damage: int = random.randint(1, 100)  # random damage per enemy
        self.maximum_number_of_enemies: int
        self.battle_flag: bool = False
        if self.battle_difficulty is BattleDifficulty.MEDIUM:
            self.maximum_number_of_enemies = 10
        elif self.battle_difficulty is BattleDifficulty.HARD:
            self.maximum_number_of_enemies = 15
        else:
            self.maximum_number_of_enemies = 6
        self.number_of_enemies: int = random.randint(1, self.maximum_number_of_enemies)

    def start_battle(self):
        self.battle_flag = True

    def attack_calculation(self):
        if self.battle_flag:
            if self.number_of_enemies > 0:
                self.number_of_enemies -= self.__player_stats.deal_damage()  # TODO: using dynamic damage lets us just fill up features later
                for i in range(self.number_of_enemies):
                    self.__player_stats.set_health(
                        self.__player_stats.health() - (self.__enemy_damage - (
                            self.__player_stats.armour_class())))  # TODO: something like this for armor, might not be used
            statmessage = "There are" + str(self.number_of_enemies) + "remaining. I have" + str(self.__player_stats.health()) + "health left."
            Speech.say(statmessage)
            if self.__player_stats.health() < 1:
                with open('images/picture.txt', "w") as f:
                    f.write('images/dead.png')
                Speech.say("I am DEAD")
                print('you stupid loser idiot haha')
            if self.number_of_enemies < 0 or not self.battle_flag:
                self.number_of_enemies = 0
                self.battle_flag = False
                Speech.say("battle win")
                print('battle win')  # TODO: placeholder, do callback to something here

    def flee(self):
        Speech.say("I AM FLEEING")
        self.battle_flag = False
        self.__player_stats.update_fleeing(True)
