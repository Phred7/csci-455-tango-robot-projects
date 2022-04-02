from typing import Dict, List


class TangoChatFileParser:

    def __init__(self, chat_file: str) -> None:
        self.user_variables: Dict[str: str] = {}
        self.word_sets: Dict[str: List[str]] = {}
        self.word_map: Dict[(str, str): str] = {}  # Ex: (u1, do you remember my name), Yes
        self.chat_file: str = chat_file
        self.level: int = 0
        self.past_valid_input: str = ""
        self.__parse()
        self.sample_dict = {(0, '~greetings'): ['hi', 'hello', "what up", 'sup'],
                            (1, 'you'): 'good',
                            (1, 'and'): ['one', 'two'],
                            (0, 'test'): 'two',
                            (0, 'my name is _'): 'hello $name',
                            (1, 'I am _ years old'): "You are $age years old",
                            (1, 'do you remember my name'): 'Yes',
                            (2, 'what is it'): '$name',
                            (3, 'you are very smart'): 'I know',
                            (0, 'what is my name'): 'your name is $name',
                            (0, 'how old am I'): 'you are $age'}

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

    def user_input(self, userinput):



        pass


if __name__ == "__main__":
    tcfp: TangoChatFileParser = TangoChatFileParser(chat_file="tango_chat.txt")

