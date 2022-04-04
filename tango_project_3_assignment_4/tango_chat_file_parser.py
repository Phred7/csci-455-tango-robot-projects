import re
from typing import Dict, List

import treelib as treelib


class TangoChatFileParser:

    def __init__(self, chat_file: str) -> None:
        self.__line_number: int = 0
        self.__file_iterator: iter = None
        self.pattern_for_matching_variables: str = """~(\w+):\s*\[(((\w+)|\s)|"((\w+(\s|)+)+)")+\]"""
        self.pattern_for_matching_u_line: str = r"""^(\s|\t)*u\d*:\s?\(~?(\w+\s?)+\)\s?:\s?((\$?\w+\s?)+|(\[(((\w+)|\s)|"((\w+(\s|)+)+)")+\]))(\n|\s|\t|\r)*$"""
        self.user_variables: Dict[str: str] = {}
        self.word_sets: Dict[str: List[str]] = {}
        self.word_map: Dict[(str, str): str] = {}
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
            self.__file_iterator = iter(chat_file)
            line: str = self.__next_line()
            try:
                while not end_of_file:
                    if "#" in line:
                        line = line[:line.index("#")]
                    if self.syntax_errors(line):
                        print(f"Syntax error on line {self.__line_number}:\'{line}\'")
                        line = self.__next_line()
                        continue
                    if len(line) < 1:
                        line = self.__next_line()
                        continue
                    variable_match = re.match(self.pattern_for_matching_variables, line, flags=re.IGNORECASE)
                    if variable_match is not None:
                        line_inputs: str = line.split(":")[1]
                        line_inputs = line_inputs[line_inputs.index('[')+1:line_inputs.index(']')]
                        user_variable_inputs: List[str] = []
                        matches = [x.group() for x in re.finditer("""(((\w+)|\s)|"((\w+(\s|)+)+)")""", line_inputs, flags=re.IGNORECASE)]
                        for match in matches:
                            if match == " ":
                                continue
                            user_variable_inputs.append(match.replace("\"", ""))
                        self.word_sets[line[line.index("~"):line.index(":")]] = user_variable_inputs
                    else:
                        # u matching
                        # dict: {u0_input_string: treelib.tree}
                        # tree: root is a node representing the first u in a set.
                        # children are u's under a u (no number) tag. Ie. u1-n's
                        # process... assume any line here is a u (without a number)
                        # create a new node to for this line.
                        # create a new tree. Make that node the root.
                        # for each u# under this u make a new node and connect them to the tree
                        # add the u0 input and the tree to the word_map dict.
                        pass

                    line = self.__next_line()

            except StopIteration:
                end_of_file = True
                self.__file_iterator = None
        pass

    def __next_line(self) -> str:
        self.__line_number += 1
        return next(self.__file_iterator)

    def user_input(self, level, _input):
        pass

    def new_node(self, u_number: int, u_input, u_response) -> treelib.Node:
        return treelib.Node(tag=u_input, identifier=u_number, data=u_response)


    def syntax_errors(self, line: str) -> bool:
        """
        Checks for syntax errors on the line in this chat_file.
        :param line: str representation of the line to check for syntax errors.
        :return: True if syntax errors were found in this chat_file otherwise, False.
        """
        # for matching in strings brackets: \[(((\w+)|\s)|"((\w+(\s|)+)+)")+\]
        # for matching strings: (\$?\w+\s?)+
        if re.match(line, r"^(\n|\s|\t|\r)*$", flags=re.X) is not None or line == "":
            return False
        variable_match = re.match(self.pattern_for_matching_variables, line, flags=re.IGNORECASE)
        u_match = re.match(self.pattern_for_matching_u_line, line, flags=re.IGNORECASE)
        if variable_match is None and u_match is None:
            return True
        return not ((variable_match is not None) != (u_match is not None))  # this is an inline xor


if __name__ == "__main__":
    tcfp: TangoChatFileParser = TangoChatFileParser(chat_file="tango_chat.txt")
    pass

