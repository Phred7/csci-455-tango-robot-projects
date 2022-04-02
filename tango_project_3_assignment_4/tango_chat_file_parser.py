
class TangoChatFileParser:

    def __init__(self, chat_file: str) -> None:
        self.chat_file: str = chat_file
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