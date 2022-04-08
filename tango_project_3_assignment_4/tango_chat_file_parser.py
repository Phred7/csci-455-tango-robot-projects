import re
from copy import deepcopy
from typing import Dict, List
import random
from treelib import Tree


class TangoChatFileParser:

    def __init__(self, chat_file: str) -> None:
        self.__line_number: int = 0
        self.__file_iterator: iter = None
        self.pattern_for_matching_variables: str = """~(\w+):\s*\[(((\w+)|\s)|"((\w+(\s|)+)+)")+\]"""
        self.pattern_for_matching_u_line: str = r"""^(\s|\t)*u\d*:\s?\(~?(\w+\s?)+\)\s?:\s?((\$?\w+\s?)+|(\[(((\w+)|\s)|"((\w+(\s|)+)+)")+\]))(\n|\s|\t|\r)*$"""
        self.user_variables: Dict[str: str] = {}
        self.word_sets: Dict[str: List[str]] = {}
        self.word_map: Dict[str: Tree] = {}
        self.chat_file: str = chat_file
        self.level: int = 0
        self.current_tree: str = None
        self.past_valid_input: str = None
        self.current_node = None
        self.__parse()

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
                        if line.isspace():
                            line = self.__next_line()
                            continue
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
                        line_inputs = line_inputs[line_inputs.index('[') + 1:line_inputs.index(']')]
                        user_variable_inputs: List[str] = []
                        matches = [x.group() for x in
                                   re.finditer("""(((\w+)|\s)|"((\w+(\s|)+)+)")""", line_inputs, flags=re.IGNORECASE)]
                        for match in matches:
                            if match == " ":
                                continue
                            user_variable_inputs.append(match.replace("\"", ""))
                        self.word_sets[line[line.index("~"):line.index(":")]] = user_variable_inputs
                    else:
                        u_tree: Tree = Tree()
                        user_input: str = line[line.index('(') + 1:line.index(')')]
                        user_response: str = line[line.index(')'):]
                        if '\n' in user_response:
                            user_response = user_response[user_response.index(':') + 1:user_response.index('\n')]
                        else:
                            user_response = user_response[user_response.index(':') + 1:]
                        u_tree.create_node(tag=0, identifier=user_input, data=self.bracketizer(user_response))

                        try:
                            line = self.__next_line()
                        except StopIteration:
                            end_of_file = True
                            self.__file_iterator = None
                            self.word_map[user_input] = deepcopy(u_tree)
                        last_number: int = 0

                        stack_list = [user_input]
                        while re.match(r"^u:", line, re.IGNORECASE) is None:
                            if "#" in line:
                                line = line[:line.index("#")]
                                if line.isspace():
                                    line = self.__next_line()
                                    continue
                            if self.syntax_errors(line):
                                print(f"Syntax error on line {self.__line_number}:\'{line}\'")
                                line = self.__next_line()
                                continue
                            if len(line) < 1:
                                line = self.__next_line()
                                continue
                            u_number = int(line[line.index('u') + 1:line.index(':')])
                            user_input = line[line.index('(') + 1:line.index(')')]
                            user_response: str = line[line.index(')'):]
                            user_response = user_response[user_response.index(':') + 1:user_response.index('\n')]
                            if last_number > u_number:
                                stack_list = stack_list[:u_number]
                            if len(stack_list) - 1 < u_number:
                                stack_list.append(user_input)
                            elif len(stack_list) - 1 == u_number:
                                stack_list[u_number] = user_input
                            u_tree.create_node(tag=u_number, identifier=user_input,
                                               data=self.bracketizer(user_response), parent=stack_list[u_number - 1])
                            last_number = u_number
                            line = self.__next_line()
                        self.word_map[stack_list[0]] = deepcopy(u_tree)
                        continue

                    line = self.__next_line()

            except StopIteration:
                end_of_file = True
                self.__file_iterator = None
        pass

    def __next_line(self) -> str:
        self.__line_number += 1
        return str(next(self.__file_iterator)).lower()

    def bracketizer(self, input):
        if "[" in input:
            output = []
            matches = [x.group() for x in
                       re.finditer("""(((\w+)|\s)|"((\w+(\s|)+)+)")""", input, flags=re.IGNORECASE)]
            for match in matches:
                if match == " ":
                    continue
                output.append(match.replace("\"", ""))
            return output
        else:
            return input

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
            vars_name = re.findall(r'\$\w+', reply)
            try:
                reply = reply.replace(vars_name[0], self.user_variables.get(vars_name[0]))
            except TypeError or KeyError:
                reply = reply.replace(vars_name[0], "UNKNOWN VALUE")
        return reply

    def check_input_with_current_lvl(self, keys_on_level, _input, bottomLevel=False):
        reply = False

        for k in keys_on_level:
            if bottomLevel: self.current_tree = k
            if '_' in k:
                k_substring = k[:k.index('_')]  # might need to add a -1 if it gets mad
                if k_substring in _input:
                    # set the variable
                    reply = self.word_map.get(self.current_tree).get_node(k).data
                    self.past_valid_input = k
                    self.level = self.word_map.get(self.current_tree).get_node(k).tag

                    var_name = re.findall(r'\$\w+', reply)  # ex $name
                    var = _input[k.index('_'):].split(' ', 1)[0]  # what the user said their name was ex Steven
                    self.user_variables[var_name[0]] = var
                    break
                else:
                    reply = False
            elif '~' in k:
                possible_valid_input = self.word_sets.get(k)
                if _input in possible_valid_input:
                    reply = self.word_map.get(self.current_tree).get_node(k).data
                    self.past_valid_input = k
                    self.level = self.word_map.get(self.current_tree).get_node(k).tag
                    break
                else:
                    reply = False
            elif _input == k:
                reply = self.word_map.get(self.current_tree).get_node(k).data
                if bottomLevel: self.current_tree = k
                self.past_valid_input = k
                self.level = self.word_map.get(self.current_tree).get_node(k).tag
                break

        # WALKER! this if statment shoudl allow for the reply to be a ~deal
        # you would still have to deal with syntax errors, but wouldnt have to
        # swap ~greetings with the list for the responses. use if helpful, dont if not
        # if isinstance(reply, str):
        #     if '~' in reply:
        #         reply = self.word_sets.get(reply)
        if isinstance(reply, list):
            reply = reply[random.randrange(0, (len(reply) - 1))]
        if isinstance(reply, str):
            reply = self.variable_swapper(reply)
        return reply

    def level_u(self, _input):
        keys_on_level = list(self.word_map.keys())
        reply = self.check_input_with_current_lvl(keys_on_level, _input, True)
        return reply

    def deeper_level(self, _input, children, node):
        keys_on_level = []

        if children:
            nodes_on_level = self.word_map.get(self.current_tree).children(node)
        else:
            nodes_on_level = self.word_map.get(self.current_tree).siblings(node)

        for n in nodes_on_level:
            keys_on_level.append(n.identifier)

        reply = self.check_input_with_current_lvl(keys_on_level, _input)
        return reply

    def user_input(self, _input):
        _input = _input.lower()  # sterilize input
        reply = False
        round = 1
        current_level = self.level
        self.current_node = self.past_valid_input

        if self.current_tree is None:  # first time through! we have nothing yet
            reply = self.level_u(_input)
        else:
            while not reply:
                if current_level == -1 and round != 1:  # we made it back to the roots of the trees
                    reply = self.level_u(_input)
                else:  # we are in a tree somewhere
                    if round == 1:
                        reply = self.deeper_level(_input, True, self.past_valid_input)
                        if isinstance(reply, str): break
                    elif round == 2:
                        reply = self.deeper_level(_input, False, self.past_valid_input)
                        if isinstance(reply, str): break
                    else:
                        if current_level > 0:
                            print(self.current_node)
                            parent = self.word_map.get(self.current_tree).parent(self.current_node)
                            reply = self.level_u(_input)
                        else:
                            parent = self.current_node
                            reply = self.deeper_level(_input, False, parent)
                        # look at parents until we reach top
                        self.current_node = parent
                        if isinstance(reply, str):
                            self.level = self.level - round + 1
                            break
                    round += 1
                current_level -= 1

        # after all possible levels checked
        if not reply:
            return "Not valid input"
        else:
            return reply


if __name__ == "__main__":
    tcfp: TangoChatFileParser = TangoChatFileParser(chat_file="liveDemoFile.txt")
    print(tcfp.user_input('robot'))
    pass

    # print(tcfp.user_input('how old am I'))
    # print(tcfp.user_input('my name is THUNDER'))
    # print(tcfp.user_input('test'))
    # print(tcfp.user_input('my name is STEVE'))
    # print(tcfp.user_input('I am 22 years old'))
    # print(tcfp.user_input('do you remember my name'))
    # print(tcfp.user_input('what is it'))
    # print(tcfp.user_input('you are very smart'))
    # print(tcfp.user_input('how old am I'))
