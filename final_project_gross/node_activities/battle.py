import random
from enum import Enum

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
        fight_string: str = f"There are {self.number_of_enemies} enemies and I have {self.__player_stats.health()} health. You must either fight or run."
        Speech.say(fight_string)
        self.battle_flag = True

    def battle(self) -> None:
        self.start_battle()
        while self.battle_flag:
            _input: str = Speech.get_speech()
            if "fight" in _input or "attack" in _input or "kill" in _input:
                self.attack_calculation()
            elif "run" in _input or "flee" in _input:
                self.flee()

    def attack_calculation(self):
        if self.battle_flag:
            if self.number_of_enemies > 0:
                self.number_of_enemies -= self.__player_stats.deal_damage()  # TODO: using dynamic damage lets us just fill up features later
                for i in range(self.number_of_enemies):
                    self.__enemy_damage = random.randint(1,100)
                    self.__player_stats.set_health(
                        self.__player_stats.health() - (self.__enemy_damage - (
                            self.__player_stats.armour_class())))  # TODO: something like this for armor, might not be used
            # TODO: logic for 0 enemies left doesnt work quite right
            if self.__player_stats.health() < 1:
                with open('images/picture.txt', "w") as f:
                    f.write('images/dead.png')
                Speech.say("I am DEAD... you stupid loser idiot haha")
                self.battle_flag = False
                return
            if self.number_of_enemies <= 0 or not self.battle_flag:
                self.number_of_enemies = 0
                self.battle_flag = False
                Speech.say("battle won, all enemies are dead.")
                say_string: str = f"I have {self.__player_stats.health()} health left."
                Speech.say(say_string)
                # TODO: placeholder, do callback to something here
            else:
                stat_message: str = f"There are {self.number_of_enemies} enemies remaining. I have {self.__player_stats.health()} health left. Fight or run."
                Speech.say(stat_message)

    def flee(self):
        Speech.say("I AM FLEEING")
        self.battle_flag = False
        self.__player_stats.update_fleeing(True)
