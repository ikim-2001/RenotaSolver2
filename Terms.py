from Feedback import *
import string

# global vars
alphabet = list(string.ascii_uppercase[::-1])


class Mistake(Problem):
    def __init__(self):
        Problem.__init__(self)
        self.curr_line = self.bad_line
        self.curr_line_left = self.curr_line.split('=')[0]
        self.curr_line_right = self.curr_line.split('=')[1]
        self.prev_line = self.prev_line
        self.terms = []
        # key = level, value = curr_line_side with unique ID's substituted for terms
        self.levels = {}
        self.levels_uncovered = {}
        self.terms_in_level = {}
        self.parse_terms_stack(self.curr_line_left, 0, "left")
        for i in range(len(self.levels)):
            self.terms_in_level[i] = []
            for term in self.terms:
                if term.count == i:
                    self.terms_in_level[i].append(f"{term.id}: "+term.content)

        print(self.curr_line_left)
        print(self.terms_in_level)
        print(self.levels)
        print(self.levels_uncovered)


    def parse_terms_stack(self, string, count, side):
        # if not initialized yet, otherwise, when recursing, subline is whatever is passed into itj

        if count not in self.levels.keys():
            self.levels[count] = string
            self.levels_uncovered[count] = string

        if string.count("(") == 0:
            terms = string.split('+')
            for item in terms:
                if item != "":
                    self.terms.append(Term(item, count, side))
                    self.terms[-1].id = str(count)+alphabet.pop()
                    self.levels[count] = self.levels[count].replace(item, self.terms[-1].id)
        else:
            stack = []
            new_str = ""
            for i in range(len(string)):
                if string[i] == "(":
                    stack.append(string[i])
                if string[i] == ")":
                    stack.pop()
                    if len(stack) == 0:
                        new_str = new_str[1:]
                        if "*(" in string:
                            others = string.replace(f"*({new_str})", "")
                        else:
                            others = string.replace(f"({new_str})", "")
                        print(f"Others: {others}, Count {count}")
                        print(f"String: {new_str}, Count {count}")
                        # print(f"Substring: {new_str}")
                        # print(f"Others: {others}")
                        self.terms.append(Term(new_str, count, side))
                        self.terms[-1].id = str(count)+alphabet.pop()
                        self.levels[count] = self.levels[count].replace(new_str, self.terms[-1].id)
                        self.parse_terms_stack(others, count, side)
                        self.parse_terms_stack(new_str, count + 1, side)
                if len(stack) > 0:
                    new_str += string[i]
        # print(f"String:{string}\nCount:{count}\nSubline:{subline}\n")

class Term():
    def __init__(self, content, count, side):
        self.content = content
        self.side = side
        self.count = count
        self.id = None





Mistake()
