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
                    line = next(chat_file)
                    # check errers
                    if "#" in line:
                        line = line[:line.index("#")]
                    elif "~" in line:
                        wordgrouplist = []
                        words = line[line.index(":")+1:]
                        if(words[0]==" "):
                            words = words [1:]
                        quote = False
                        prevInd = 1
                        for ind in range(0, len(words)):
                            #print("Ind is:",ind,"Char is",words[ind])
                            if words[ind] == "\"":
                                quote = not quote
                            elif words[ind] == " " and not quote or words[ind] == "]":
                                #remove quotes
                                #words.replace("\"","")
                                #do this to the list after iterating
                                wordgrouplist.append(words[prevInd:ind])
                                print(wordgrouplist)
                                prevInd = ind +1
                        self.word_sets[line[line.index("~"):line.index(":")]] = wordgrouplist
                    elif "$" in line:
                        pass
                    else:
                        pass
                    # parser here
                print(self.word_sets)
            except StopIteration:
                end_of_file = True

    def user_input(self, level, input):
        pass


if __name__ == "__main__":
    tcfp: TangoChatFileParser = TangoChatFileParser(chat_file="tildetest.txt")
