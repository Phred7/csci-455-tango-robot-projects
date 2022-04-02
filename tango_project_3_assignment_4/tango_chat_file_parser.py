from typing import Dict, List


class TangoChatFileParser:

    def __init__(self, chat_file: str) -> None:
        self.user_variables: Dict[str: str] = {}
        self.word_sets: Dict[str: List[str]] = {}
        self.word_map: Dict[(str, str): str] = {}
        self.chat_file: str = chat_file
        self.level: int = 0
        self.past_valid_input: str = None
        self.__parse()
        pass

    def __parse(self):
        end_of_file: bool = False
        with open(self.chat_file, 'r') as chat_file:
            chat_file = iter(chat_file)
            line: str = ""
            try:
                while not end_of_file:
                    # line = next(chat_file)
                    # parser here
                    pass
            except StopIteration:
                end_of_file = True
        pass

    def user_input(self, level, input):
        pass


if __name__ == "__main__":
    tcfp: TangoChatFileParser = TangoChatFileParser(chat_file="tango_chat.txt")
