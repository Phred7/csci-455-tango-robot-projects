import re
from typing import Dict, List
import random
import treelib as treelib
import re


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
        self.current_tree: str = None
        self.past_valid_input: str = None
        self.current_node = None
        self.__parse()
        self.sample_dict = {(0, '~greetings'): ['hi', 'hello', "what up", 'sup'],
                            (1, 'you'): '~greetings',
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
                    # need to sterilize input - all lowercase? or all upper..
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

    def variable_swapper(self, reply):
        '''
        takes in the reply and puts a variable in place of $var
        :param reply:
        :return:
        '''
        # swaps '$Name' for 'Chloe'
        if '$' in reply:
            list_of_vars = re.findall(r'\$\w+', reply)
            for v in list_of_vars:
                try:
                    reply.replace(list_of_vars[v], self.user_variables.get(v))
                except KeyError:
                    reply.replace(list_of_vars[v], 'UNKNOWN VALUE')
        return reply

    def check_input_with_current_lvl(self, keys_on_level, _input, *, bottomLevel = False):
        reply = False

        for k in keys_on_level:
            if '_' in k:
                k_substring = k[:k.index('_')]  # might need to add a -1 if it gets mad
                if k_substring in _input:
                    # set the variable
                    reply = self.word_map.get(self.current_tree).get_node(k).data()
                    if bottomLevel: self.current_tree = k
                    self.past_valid_input = k
                    self.level = self.word_map.get(self.current_tree).get_node(k).tag()

                    var_name = re.findall(r'\$\w+', reply) #ex $name
                    var = _input[k.index('_'):].split(' ', 1)[0]  # what the user said their name was ex Steven
                    self.user_variables[var_name] = var
                else:
                    reply = False
            elif '~' in k:
                possible_valid_input = self.word_sets.get(k)
                if _input in possible_valid_input:
                    reply = self.word_map.get(self.current_tree).get_node(k).data()
                    if bottomLevel: self.current_tree = k
                    self.past_valid_input = k
                    self.level = self.word_map.get(self.current_tree).get_node(k).tag()
                else:
                    reply = False
            elif _input is k:
                reply = self.word_map.get(self.current_tree).get_node(k).data()
                if bottomLevel: self.current_tree = k
                self.past_valid_input = k
                self.level = self.word_map.get(self.current_tree).get_node(k).tag()

        if isinstance(reply, list):
            reply = reply[random.randrange(0, (len(reply)-1))]
        if isinstance(reply, str):
            reply = self.variable_swapper(reply)
        return reply


    def user_input(self, _input):
        #need to sterilize input - all lowercase? or all upper..
        _input = _input.lower()
        reply = False
        counter = 1
        self.current_node = self.past_valid_input

        if self.current_tree is None:  # first time through! we have nothing yet
            keys_on_level = self.word_map.keys()
            reply = self.check_input_with_current_lvl(keys_on_level, _input, True)
        else:
            while not reply and self.level is not -1:
                if self.level is 0:
                    keys_on_level = self.word_map.keys()
                    reply = self.check_input_with_current_lvl(keys_on_level, _input, True)
                else:
                # get all user inputs on current U level and put it in a list
                # call check input with that list
                    if counter is 1:
                        # look at kids
                        nodes_on_level = self.word_map.get(self.current_tree).children(self.past_valid_input)
                        for n in nodes_on_level:
                            keys_on_level.append(n.identifier)
                        # make it a list of just ids
                        reply = self.check_input_with_current_lvl(keys_on_level, _input)
                    if counter is 2:
                        # look at siblings
                        keys_on_level = self.word_map.get(self.current_tree).siblings(self.past_valid_input)
                        for n in nodes_on_level:
                            keys_on_level.append(n.identifier)
                        # make it a list of just ids
                        reply = self.check_input_with_current_lvl(keys_on_level, _input)
                    else:
                        parent = self.word_map.get(self.current_tree).siblings(self.current_node)
                        keys_on_level = self.word_map.get(self.current_tree).siblings(parent)
                        for n in nodes_on_level:
                            keys_on_level.append(n.identifier)
                        # look at parents until we reach top
                        reply = self.check_input_with_current_lvl(keys_on_level, _input)
                        self.current_node = parent
                    counter += 1
                    self.level -= 1

        #after all possible levels checked
        if not reply:
            return "Not valid input"
        else:
            # CONNIEE!!!! set level and parent and past valid response
            return reply

if __name__ == "__main__":
    tcfp: TangoChatFileParser = TangoChatFileParser(chat_file="tango_chat.txt")
    pass

