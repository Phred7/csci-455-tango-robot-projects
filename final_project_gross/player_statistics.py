class PlayerStatistics:
    """
    Stores and Encapsulates the Statistics for a player.
    """

    def __init__(self, player_name: str) -> None:
        self.__player_name: str = player_name
        self.__health: int = 400
        self.__damage_to_enemy: int = 1  # TODO: might not use this, depends on how fast we want 'battles' to happen
        self.__armor: int = 0  # TODO: might not use this, use with simple factorial equation to mitigate damage (dmg-x/100)
        self.__current_x = 0
        self.__current_y = 0

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

    def set_position(self, x,y): #could be tuple
        self.current_x = x
        self.current_y = y