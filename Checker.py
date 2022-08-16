from sympy import symbols, solve, Eq

import json_inequalities
from json_form import *

class Checker():
    def __init__(self, input_json):
        print(input_json)
        self.input_json = input_json
        self.text = []
        for line in input_json.values():
            self.text.append(line.replace("–", "-"))
        self.problem = self.text[0].replace(" ", "")
        self.isCorrect = None
        # fixed for now heh
        self.comparator = self.find_comparator(self.text[0])
        self.variable = self.findvar()
        self.problem = self.parse(self.problem)
        self.problem_left = self.problem.split(self.comparator)[0]
        self.problem_right = self.newlinesgone(self.problem.split(self.comparator)[-1])
        self.true_output = self.solve(self.problem_left, self.problem_right)
        self.output = self.text[-1].replace(" ", "")
        self.output = self.parse(self.output)
        self.student_left = self.output.split(self.find_comparator(self.output))[0]
        self.student_right = self.output.split(self.find_comparator(self.output))[-1]
        self.student_output = self.solve(self.student_left, self.student_right)
        self.isCorrect = self.verify()
        self.consistent_comparators = None

    def return_input_json(self):
        return self.input_json

    # returns new self.problem where coeffs are separated to
    # vars with a * (will do parenthessis later)

    def findvar(self):
        for char in self.text[0]:
            if char.isalpha():
                return char

    def newlinesgone(self, str):
        new_right = ""
        for i in range(len(str)):
            if str[i] == "\n":
                break
            new_right += str[i]
        return new_right

    # returns an array with the parsed problem as first element
    # and parsed answer as second element
    def parse(self, str):
        # print(f"Parsing: {str}")
        output = []
        new_str = ""
        # parse the problem
        # for coefficients and variables
        for i in range(len(str)):
            if str[i] == self.variable:
                # if there is a coefficient in front of variable
                if i > 0 and str[i - 1].isnumeric():
                    new_str += f"*var"
                else:
                    new_str += "var"
            elif str[i] == "(":
                # if there is a variable or number before '('
                if i > 0 and (str[i-1].isnumeric() or str[i-1].isalpha()):
                    new_str += "*("
                else:
                    new_str += "("
            elif str[i] == ")":
                # the ")" is not the last char and there is a number or variable after the str
                if i < len(str)-1:
                    if (str[i+1].isnumeric() or str[i+1].isalpha()):
                        new_str += ")*"
                    else:
                        new_str += ")"
                else:
                    new_str += ")"
            elif str[i] == "-":
                # changes the 2-x -> 2+-x; -2 -> +-2
                if i < len(str) - 1:
                    # edge case: -(2x+3) =
                    if str[i+1] == "(":
                        new_str += "+-1*"
                    else:
                        new_str += "+-"
                else:
                    new_str += "+-"
            else:
                new_str += str[i]

        return new_str

    def solve(self, lhs, rhs):
        # print(f"Solving: {self.problem}")
        var = symbols(self.variable)
        lhs = eval(lhs)
        rhs = eval(rhs)
        answer = str(solve(Eq(lhs, rhs), var)[0])
        # print(f"SOLVING PROBLEM: {self.problem}\nASNWER: {answer}")
        return answer

    def verify(self):
        # print(f"Student's Answer: {self.student_output}\n"
        #       f"Correct Answer: {self.solve()}")
        if self.true_output == self.student_output:
            # print("Student is correct! :)")
            return True
        # print("Student is incorrect! :(")
        return False


    def find_comparator(self, string):
        # first line is always the valid operator
        if ">=" in string or "<=" in string:
            return ">=" if ">=" in string else "<="
        elif ">" in string or "<" in string:
            return ">" if ">" in string else "<"
        else:
            return "="


