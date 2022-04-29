from typing import Tuple


class PlayerStatistics:
    """
    Encapsulates the Statistics for a player.
    """

    def __init__(self, player_name: str) -> None:
        self.__player_name: str = player_name
        self.__health: int = 400
        self.__damage_to_enemy: int = 1  # TODO: might not use this, depends on how fast we want 'battles' to happen
        self.__armor: int = 0  # TODO: might not use this, use with simple factorial equation to mitigate damage (dmg-x/100)
        self.__current_x: int = 0
        self.__current_y: int = 0
        self.__direction_facing: str = "north"
        self.__fleeing: bool = False

    def health(self) -> int:
        return self.__health

    def modify_health(self, modification: int) -> None:
        self.__health += modification

    def set_health(self, health: int):
        self.__health = health

    def player_name(self) -> str:
        return self.__player_name

    def deal_damage(self) -> int:   # TODO: may want this to return a random value in a range.
        return self.__damage_to_enemy

    def armour_class(self) -> int:
        return self.__armor

    def modify_armour_class(self, new_armour_class: int) -> None:
        self.__armor = new_armour_class

    def fleeing(self) -> bool:
        return self.__fleeing

    def update_fleeing(self, isfleeing: bool) -> None:
        self.__fleeing = isfleeing

    def direction_facing(self) -> str:
        return self.__direction_facing

    def change_direction_facing(self, direction: str) -> None:
        if direction == "north" or direction == "south" or direction == "east" or direction == "west":
            self.__direction_facing = direction
            return
        raise ValueError

    def current_position(self) -> Tuple[int, int]:
        return self.__current_x, self.__current_y

    def update_current_position(self, x: int, y: int) -> None:
        self.__current_x = x
        self.__current_y = y