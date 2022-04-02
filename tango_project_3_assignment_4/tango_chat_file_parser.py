
class TangoChatFileParser:

    def __init__(self, chat_file: str) -> None:
        self.chat_file: str = chat_file
        self.__parse()
        pass

    def __parse(self):
        with open(self.chat_file, 'r') as chat_file:
            chat_file = iter(chat_file)
            line: str = ""
        pass