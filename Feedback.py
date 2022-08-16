from Checker import *
# use Checker().isCorSErect to display the lines in which there is

class Problem(Checker):
    def __init__(self):
        Checker.__init__(self)
        # print("\n")
        self.lines = self.text.copy()
        self.no_slash_n()
        self.lines = self.instantiate_lines(self.lines)
        # bad line refers to the line in which person fucked up
        self.array = self.iterate_lines(self.lines)
        self.parsed_prev_line = self.array[0][0].replace(' ', "")
        self.parsed_curr_line = self.array[0][1].replace(' ', "")
        self.unparsed_prev_line = self.array[1][0].replace(' ', "")
        self.unparsed_curr_line = self.array[1][1].replace(' ', "")
        # print(self.unparsed_prev_line.split("=")[0])
        # self.n_1_left = Term(1, self.unparsed_prev_line.split("=")[0], {"x": self.true_output, "": 1}, {"1's": 0, "x's": 0})
        # self.n_1_right = Term(1, self.unparsed_prev_line.split("=")[1], {"x": self.true_output, "": 1}, {"1's": 0, "x's": 0})
        # self.n_left = Term(1, self.unparsed_curr_line.split("=")[0], {"x": self.true_output, "": 1}, {"1's": 0, "x's": 0})
        # self.n_right = Term(1, self.unparsed_curr_line.split("=")[1], {"x": self.true_output, "": 1}, {"1's": 0, "x's": 0})

    # gets rid of that \n
    def no_slash_n(self):
        for i in range(len(self.lines)):
            self.lines[i] = self.parse(self.lines[i].replace("\n", ""))[0].replace(" ", "")

    # replace these lines from being strings to -> Line() struct type
    def instantiate_lines(self, array):
        # print("Showing student's work:")
        for i in range(len(array)):
            array[i] = Line(array[i])
            # print(array[i].content)
        # print("\n")
        return array


    # iterates through the array and checks which part is wrong
    def iterate_lines(self, array):
        for i in range(len(array)):
            # is wrong if the answer is off by the nearest thousandth
            if abs(eval(array[i].left_side.replace("var", self.true_output)) - eval(array[i].right_side.replace("var", self.true_output))) >= 0.01:
                # print(f"Feedback: You fucked up between:\n"
                #       f"Line {int(i)} : {array[i-1].content}\n"
                #       f"Line {int(i+1)}: {array[i].content}\n")

                return [(array[i-1].content, array[i].content), (self.text[i-1], self.text[i])]

class Line():
    def __init__(self, content):
        self.content = content
        self.left_side = self.content.split("=")[0]
        self.right_side = self.content.split("=")[-1]