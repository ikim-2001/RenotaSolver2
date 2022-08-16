import copy
from sympy import symbols, solve, Eq
from Checker import *
from Terms2 import *
from collections import deque


class findMistakeTerms():
    def find_cons_vars_diff(self, term1, term2):
        diff_dict = {"x": 0, "1": 0}
        t1dict = term1.constants_vars_dict
        t2dict = term2.constants_vars_dict
        base_kinds = []

        if t1dict["x's"] != t2dict["x's"]:
            diff_dict["x"] = t1dict["x's"] - t2dict["x's"]
        if t1dict["1's"] != t2dict["1's"]:
            diff_dict["1"] = t1dict["1's"] - t2dict["1's"]
        # difference in both
        if diff_dict["x"] == 0:
            base_kinds.append("x")
        if diff_dict["1"] == 0:
            base_kinds.append("1")
        return base_kinds

    # call this method twice: once on left and once on right
    def remove_potential_terms(self, term1, term2, term_list):
        term_type = self.find_cons_vars_diff(term1, term2)
        return_list = []
        for term in term_list:
            if len(term.xs_ones_both) == 1 and term.xs_ones_both[0] not in term_type:
                return_list.append(term)
            # coeffs are always potential problems
            elif len(term.xs_ones_both) == 2:
                return_list.append(term)
        return return_list

    # terms that were in line n-1 that are still in line
    # takes in removed_left and left_n_1.potential_problem_terms

    def remove_preexisting_terms(self, term_list_1, term_list_2):
        # in order of all the coeffs
        coeffs = list(map(Term.get_coef, term_list_2))
        contents = list(map(Term.get_content, term_list_2))
        stack_levels = list(map(Term.get_stack_level, term_list_2))
        coeffs2 = list(map(Term.get_coef, term_list_1))
        contents2 = list(map(Term.get_content, term_list_1))
        stack_levels2 = list(map(Term.get_stack_level, term_list_1))
        ret_list = term_list_1.copy()
        # if the duplicate term is in line n-1 as in line n, remove it from line n
        # apply to left and right sides
        for term in term_list_1:
            for i in range(len(coeffs)):
                # same coeff
                if term.term_coefficient == coeffs[i]:
                    if stack_levels[i] == term.input_stack_level and contents[i] == term.term_content:
                        ret_list.remove(term)
                    continue
        return ret_list

    def remove_termsoperators_both_sides(self, left_possible_operands, right_possible_operands, left_potential_terms,
                                         right_potential_terms):
        # if adding x's on left and right are the same, then eliminate terms that are x field in left and right
        total = left_potential_terms + right_potential_terms
        targeted_term = ""
        if left_possible_operands[0]['x'] == right_possible_operands[0]['x'] and right_possible_operands[0]["x"]:
            targeted_term += "x"
        if left_possible_operands[0]["1"] == right_possible_operands[0]["1"] and right_possible_operands[0]["1"]:
            targeted_term += "1"
        if left_possible_operands[1]["ratio"] == right_possible_operands[1]["ratio"] and right_possible_operands[1][
            "ratio"]:
            targeted_term += "x1"
        return self.remove_terms_given_curr_type_and_array(targeted_term,
                                                           left_potential_terms), self.remove_terms_given_curr_type_and_array(
            targeted_term, right_potential_terms)

    # input a dict and we will remove terms that are negative inverse of the operator that we wanted (line by line)
    # found in prev line's side
    # i.e., pass in
    def iterate_negative_and_remove(self, add_dict, prev_line_term, potential_side_terms):
        stack_level = list(map(Term.get_coef, potential_side_terms))
        for key in add_dict.keys():
            # if valid operand in key:
            if add_dict[key] != None:
                # print(f"Key: {key}; Value: {add_dict[key]}")
                for term in prev_line_term.potential_problem_terms:
                    # same type of term and the iterated term is the negative inverse of the + operand
                    if abs(add_dict[key] + term.term_coefficient) < 0.1 and key == term.term_content:
                        # delete any term in potential_side_keys that have that corresponding value!!
                        potential_side_terms = self.remove_terms_given_curr_type_and_array(key, potential_side_terms)
                        # print(f"Match found!! {add_dict[key]}{key} and {term.term_coefficient}{term.term_content} are negative inverses of each other!!")
        return potential_side_terms

    def remove_terms_from_multiplicative_inverse(self, add_dict, prev_line_term, side_problem_terms):
        # if it's a valid ratio
        if add_dict["ratio"]:
            # search thru terms in prev_line_term to fidn multiplicative inverse and if you find, then reduce all terms from side_problem_terms
            for term in prev_line_term.potential_problem_terms:
                # if they are mutiplicative inverses of each other, that means that this was a valid multiplication
                if abs((term.term_coefficient * add_dict["ratio"]) - 1) < 0.01:
                    side_problem_terms = self.remove_terms_given_curr_type_and_array("x1", side_problem_terms)
                    # print(f"Match found!! {add_dict['ratio']}{'ratio'} and {term.term_coefficient}{term.term_content} are multiplicative inverses of each other!!")
        return side_problem_terms

    # given a string (1's, x's, or both that are logical operands on both left and right), erase corresponding elements
    # on line n (list of potential problem terms)
    def remove_terms_given_curr_type_and_array(self, curr_type, array):
        copied_array = copy.deepcopy(array)
        for term in array:
            # each iteration, the ids will be representative of the dynamically changing array
            ids = list(map(Term.get_id, copied_array))
            # term matches logical operand
            if term.xs_ones_both[0] in curr_type:
                index = ids.index(term.id)  # get the index of the term in ids
                # remove that element's ID in ids array
                bob = copied_array.pop(index)
                # print(f"{bob.term_coefficient}{bob.term_content}")
        return copied_array

    # four inputs are just terms in line n and line n-1 from left and right
    def determine_valid_operands(self, left, prev_left, right, prev_right, left_potential_terms, right_potential_terms):
        # first element in tuple represents dict of diffs (x's and 1's)
        # second element in tuple represents dict of ratios (x's and 1's)
        left_possible_operands, right_possible_operands = ({}, {}), ({}, {})
        # first calculate differences (for 1's and x's) between left side of line n and line n-1
        left_ones_difference = left.constants_vars_dict["1's"] - prev_left.constants_vars_dict["1's"] if \
        left.constants_vars_dict["1's"] - prev_left.constants_vars_dict["1's"] != 0 else None
        left_xs_difference = left.constants_vars_dict["x's"] - prev_left.constants_vars_dict["x's"] if \
        left.constants_vars_dict["x's"] - prev_left.constants_vars_dict["x's"] != 0 else None
        right_ones_difference = right.constants_vars_dict["1's"] - prev_right.constants_vars_dict["1's"] if \
        right.constants_vars_dict["1's"] - prev_right.constants_vars_dict["1's"] != 0 else None
        right_xs_difference = right.constants_vars_dict["x's"] - prev_right.constants_vars_dict["x's"] if \
        right.constants_vars_dict["x's"] - prev_right.constants_vars_dict["x's"] != 0 else None

        # next calculate the ratios of the shitters
        # must compare the ratios of the 1's and x's if they are same, if yes, then store into dict
        left_ones_ratio = left.constants_vars_dict["1's"] / prev_left.constants_vars_dict["1's"] if \
        prev_left.constants_vars_dict["1's"] != 0 else None
        left_xs_ratio = left.constants_vars_dict["x's"] / prev_left.constants_vars_dict["x's"] if \
        prev_left.constants_vars_dict["x's"] != 0 else None
        right_ones_ratio = right.constants_vars_dict["1's"] / prev_right.constants_vars_dict["1's"] if \
        prev_right.constants_vars_dict["1's"] != 0 else None
        right_xs_ratio = right.constants_vars_dict["x's"] / prev_right.constants_vars_dict["x's"] if \
        prev_right.constants_vars_dict["x's"] != 0 else None

        # for adding
        left_possible_operands[0]["1"], left_possible_operands[0]["x"] = left_ones_difference, left_xs_difference
        right_possible_operands[0]["1"], right_possible_operands[0]["x"] = right_ones_difference, right_xs_difference
        # print(f"right ratio ones {right_ones_ratio}\nright ratio xs {right_xs_ratio}")

        # for multiplying, the ratios of both data types are the same so we set to both
        if left_ones_ratio and left_xs_ratio:
            left_possible_operands[1]["ratio"] = left_ones_ratio if left_ones_ratio == left_xs_ratio else None
        # one of them is None meaning, one of them None
        else:
            left_possible_operands[1]["ratio"] = None

        if right_ones_ratio and right_xs_ratio:
            right_possible_operands[1]["ratio"] = right_ones_ratio if right_ones_ratio == right_xs_ratio else None
        # one of them is None meaning, one of them None
        else:
            right_possible_operands[1]["ratio"] = None

        return (left_possible_operands, right_possible_operands)


class Main():

    def __init__(self, input_json):
        self.check = Checker(input_json)
        self.incorrect_line = (0, None)
        self.prev_incorrect_line = (0, None)
        self.total_potential_terms = []
        self.variable = self.check.variable
        self.original_text = copy.deepcopy(self.check.text)
        self.output_lines = [self.check.text[0]]
        self.incorrect_indices = []
        self.trueIsCorrect = copy.deepcopy(self.check.isCorrect)
        self.untouchable = copy.deepcopy(self.check.text)
        self.index_wrong_comparators = {}
        fmt = findMistakeTerms()

    # method that checks if correct
    def verify_answer(self):
        self.check.verify()

    # return a boolean value after comparing left and right sides
    # valid inflection, valid 1% greater, valid 1% less
    def three_comparators(self, left, right, comparator):
        # print(f"Comparing {left.term_content} {comparator} {right.term_content}")
        return_array = [None, None, None]
        if comparator == "=":
            comparator = "=="
        # print("INFLECTION")
        # print(f"{str(left.evaluate()) + comparator + str(right.evaluate())}")
        if eval(str(left.evaluate()) + comparator + str(right.evaluate())):
            return_array[0] = True
        # print("GREATER")
        # print(left.toggle("upper"), comparator, right.toggle("upper"))
        if eval(str(left.toggle("upper")) + comparator + str(right.toggle("upper"))):
            return_array[1] = True
        # print("LESSER")
        # print(left.toggle("lower"), comparator, right.toggle("lower"))
        if eval(str(left.toggle("lower")) + comparator + str(right.toggle("lower"))):
            return_array[2] = True
        # print(return_array)
        # print("\n")

        return return_array


    def check_consistent_comparators(self):
        # this will update every foor loop so thus, when this is called this will too and so will the boolean triple
        first_comparator = self.check.find_comparator(self.check.text[0])
        last_comparator = self.check.find_comparator(self.check.text[-1])
        first_left = Term(1, self.check.text[0].strip().split(first_comparator)[0].replace(" ", "").replace(self.variable, "x"), {"x": eval(self.check.true_output), "": 1}, {"x": eval(self.check.true_output)*2, "": 1},
                                      {"x": eval(self.check.true_output)/2, "": 1}, {"1's": 0, "x's": 0}, 0)
        first_right = Term(1, self.check.text[0].strip().split(first_comparator)[1].replace(" ", "").replace(self.variable, "x"), {"x": eval(self.check.true_output), "": 1}, {"x": eval(self.check.true_output)*2, "": 1},
                                      {"x": eval(self.check.true_output)/2, "": 1}, {"1's": 0, "x's": 0}, 0)
        last_left = Term(1, self.check.text[-1].strip().split(last_comparator)[0].replace(" ", "").replace(self.variable, "x"), {"x": eval(self.check.true_output), "": 1}, {"x": eval(self.check.true_output)*2, "": 1},
                                      {"x": eval(self.check.true_output)/2, "": 1}, {"1's": 0, "x's": 0}, 0)
        last_right = Term(1, self.check.text[-1].strip().split(last_comparator)[1].replace(" ", "").replace(self.variable, "x"), {"x": eval(self.check.true_output), "": 1}, {"x": eval(self.check.true_output)*2, "": 1},
                                      {"x": eval(self.check.true_output)/2, "": 1}, {"1's": 0, "x's": 0}, 0)
        # print(f"FIRST LINE: {first_left.term_content} {first_comparator} {first_right.term_content}")
        # print(f"LAST LINE: {last_left.term_content} {last_comparator} {last_right.term_content}")
        # boolean triple refers to the inequality holding if:
        # 1) inflection point is inputted
        # 2) inflection point * 1.01 is inputted
        # 3) inflection point * 0.99 is inputted
        first_boolean_triple = self.three_comparators(first_left, first_right, first_comparator)
        last_boolean_triple = self.three_comparators(last_left, last_right, last_comparator)
        # print(first_boolean_triple)
        # print(last_boolean_triple)
        if first_boolean_triple == last_boolean_triple:
            self.check.consistent_comparators = True
        else:
            self.check.consistent_comparators = False

    def find_inflection(self, left, right):
        var = symbols(self.variable)
        lhs, rhs = self.check.parse(left), self.check.parse(right)
        lhs = eval(lhs)
        rhs = eval(rhs)
        answer = str(solve(Eq(lhs, rhs), var)[0])
        return answer

    # given that line n-1 and line n have different
    # inflection points, we must find a valid solution of
    # line n-1 and plug that into line n. if it still holds, then line
    # line comparator is valid. else, add it to the incorrect indices list


    # returns a list of potential terms wrong
    def find_mistake_terms(self):
        # fmt acronym
        global curr_comparator, old_comparator
        fmt = findMistakeTerms()
        prev_left_side, prev_right_side = None, None
        # in thec ase that it's none
        if len(self.check.text) <= 1:
            return []
        for i in range(1, len(self.check.text)):
            old_comparator = self.check.find_comparator(self.check.text[i - 1])
            curr_comparator = self.check.find_comparator(self.check.text[i])
            left_side_content = self.check.text[i].strip().split(curr_comparator)[0].replace(" ", "")
            right_side_content = self.check.text[i].strip().split(curr_comparator)[1].replace(" ", "")
            prev_left_side_content = self.check.text[i-1].strip().split(old_comparator)[0].replace(" ", "")
            prev_right_side_content = self.check.text[i-1].strip().split(old_comparator)[1].replace(" ", "")
            prev_inflection = self.find_inflection(prev_left_side_content, prev_right_side_content)
            curr_inflection = self.find_inflection(left_side_content, right_side_content)

            left_side = Term(1, self.check.text[i].strip().split(curr_comparator)[0].replace(" ", "").replace(
                self.variable, "x"),
                             {"x": eval(self.check.true_output), "": 1}, {"x": float(eval(curr_inflection))+1, "": 1},
                             {"x": float(eval(curr_inflection))-1, "": 1}, {"1's": 0, "x's": 0}, 0)
            right_side = Term(1, self.check.text[i].strip().split(curr_comparator)[1].replace(" ", "").replace(
                self.variable, "x"),
                              {"x": eval(self.check.true_output), "": 1},
                              {"x": float(eval(curr_inflection))+1, "": 1},
                              {"x": float(eval(curr_inflection))-1, "": 1}, {"1's": 0, "x's": 0}, 0)
            # condition in which we find the wrong line
            prev_left_side = Term(1,
                                  self.check.text[i - 1].strip().split(old_comparator)[0].replace(" ", "").replace(
                                      self.variable, "x"),
                                  {"x": eval(self.check.true_output), "": 1},
                                  {"x": float(eval(prev_inflection))+1, "": 1},
                                  {"x": float(eval(prev_inflection))-1, "": 1}, {"1's": 0, "x's": 0}, 0)
            prev_right_side = Term(1,
                                   self.check.text[i - 1].strip().split(old_comparator)[1].replace(" ", "").replace(
                                       self.variable, "x"),
                                   {"x": eval(self.check.true_output), "": 1},
                                   {"x":float(eval(curr_inflection))+1, "": 1},
                                   {"x": float(eval(curr_inflection))-1, "": 1}, {"1's": 0, "x's": 0}, 0)

            left_side_ineq, right_side_ineq = copy.deepcopy(left_side), copy.deepcopy(right_side)
            prev_left_side_ineq, prev_right_side_ineq = copy.deepcopy(prev_left_side), copy.deepcopy(prev_right_side)
            left_side_ineq.input_string_lookup_dict["x"], right_side_ineq.input_string_lookup_dict["x"] = eval(curr_inflection), eval(curr_inflection)
            prev_left_side_ineq.input_string_lookup_dict["x"] = eval(prev_inflection)
            prev_right_side_ineq.input_string_lookup_dict["x"] = eval(prev_inflection)

            curr_bool_triple = self.three_comparators(left_side_ineq, right_side_ineq, curr_comparator)
            prev_bool_triple = self.three_comparators(prev_left_side_ineq, prev_right_side_ineq, old_comparator)

            # we will stop in cases in which:
            # inflections are different!!
            # or inflections are same and the bools are different
            if abs(float(left_side.evaluate()) - float(right_side.evaluate())) > 0.01 or (curr_bool_triple != prev_bool_triple):
                # if inflections are the same but there is a difference in bool

                self.prev_incorrect_line = (i - 1, self.check.text[i - 1])
                self.incorrect_line = (i, self.check.text[i])

                # this evaluates the cons/vars
                left_side.cons_var_eval(), right_side.cons_var_eval(), prev_left_side.cons_var_eval(), prev_right_side.cons_var_eval()
                # print(left_side.constants_vars_dict)
                # ###### THE INEQUALITIES CHCKER ###############

                if curr_bool_triple != prev_bool_triple and curr_comparator != "=" and curr_comparator != "=":
                    if curr_inflection == prev_inflection:
                        ind = self.untouchable.index(self.check.text[i])
                        self.index_wrong_comparators[ind] = curr_comparator
                    else:
                        if curr_comparator != old_comparator:
                            ind = self.untouchable.index(self.check.text[i])
                            self.index_wrong_comparators[ind] = curr_comparator


                left_potential_terms = fmt.remove_potential_terms(left_side, prev_left_side,
                                                                  left_side.potential_problem_terms)
                right_potential_terms = fmt.remove_potential_terms(right_side, prev_right_side,
                                                                   right_side.potential_problem_terms)

                self.total_potential_terms = left_potential_terms + right_potential_terms
                # print("STEP 1: Remove terms by total 1's and x's count in each side ")
                list_of_terms = []
                for term in left_potential_terms + right_potential_terms:
                    list_of_terms.append(f"{term.term_coefficient}{term.term_content}")
                if len(self.total_potential_terms) <= 1:
                    return self.total_potential_terms
                # print(f"Remaining Terms: {list_of_terms}\n")
                left_line_compare, right_line_compare = prev_left_side.potential_problem_terms, prev_right_side.potential_problem_terms
                left_potential_terms, right_potential_terms = fmt.remove_preexisting_terms(left_potential_terms,
                                                                                           left_line_compare), fmt.remove_preexisting_terms(
                    right_potential_terms, right_line_compare)
                # print("STEP 2: Remove terms found in line n that are also found in line n-1")
                self.total_potential_terms = left_potential_terms + right_potential_terms
                return_array = []
                for term in self.total_potential_terms:
                    str = f"{term.term_coefficient}{term.term_content}"
                    return_array.append(str)
                # print(f"{return_array}\n")
                if len(self.total_potential_terms) <= 1:
                    return self.total_potential_terms
                # perform first two remove functions: Total Type (sum 1's and x's; and also comparing line n-1 with line n)
                if not left_potential_terms or not right_potential_terms:
                    # mistakes on the left side
                    if left_potential_terms:
                        # print("Error on left side")
                        list_of_terms = []
                        for term in left_potential_terms:
                            list_of_terms.append(f"{term.term_coefficient}{term.term_content}")
                        # print(f"Remaining Terms: {list_of_terms}\n")
                        # print("STEP 3: Remove terms found in line n that are also found in line n-1 simplified one step")
                        left_potential_terms = self.combinatorics_bfs(left_potential_terms, right_potential_terms, prev_left_side, left_side)
                        list_of_terms.clear()
                        for term in left_potential_terms:
                            list_of_terms.append(f"Remaining Terms: {term.term_coefficient}{term.term_content}")
                        # print(list_of_terms)
                        self.total_potential_terms = left_potential_terms
                        return self.total_potential_terms
                    # execute the bfs on right terms
                    elif right_potential_terms:
                        # print("Error on right side"cu)
                        list_of_terms = []
                        for term in right_potential_terms:
                            list_of_terms.append(f"{term.term_coefficient}{term.term_content}")
                        # print(f"Remaining Terms: {list_of_terms}\n")
                        # print("STEP 3: Remove terms found in line n that are also found in line n-1 simplified one step")
                        right_potential_terms = self.combinatorics_bfs(right_potential_terms, left_potential_terms, prev_right_side,
                                                                       right_side)
                        list_of_terms.clear()
                        for term in right_potential_terms:
                            list_of_terms.append(f"Remaining Terms: {term.term_coefficient}{term.term_content}")
                        # print(list_of_terms)
                        self.total_potential_terms = right_potential_terms
                        return self.total_potential_terms
                else:
                    # print("\nStep 3: Remove Terms that are types where a related calculation found on both sides")
                    # print("Errors on both sides")
                    left_possible_operands, right_possible_operands = fmt.determine_valid_operands(left_side,
                                                                                                   prev_left_side,
                                                                                                   right_side,
                                                                                                   prev_right_side,
                                                                                                   left_potential_terms,
                                                                                                   right_potential_terms)
                    left_potential_terms, right_potential_terms = fmt.remove_termsoperators_both_sides(
                        left_possible_operands, right_possible_operands, left_potential_terms, right_potential_terms)
                    self.total_potential_terms = left_potential_terms + right_potential_terms
                    # left_potential_terms, right_potential_terms = fmt.modify_left_right_pot_term_list(self.total_potential_terms, left_potential_terms, right_potential_terms)
                    return_array = []
                    for term in self.total_potential_terms:
                        str = f"{term.term_coefficient}{term.term_content}"
                        return_array.append(str)
                    # print(f"Remaining Terms: {return_array}\n")
                    if len(self.total_potential_terms) <= 1:
                        return self.total_potential_terms
                    # print("\nStep 4: Remove terms in line n where related calculation is a negative term in line n-1")
                    # print(left_possible_operands[0], right_possible_operands[0])
                    left_potential_terms = fmt.iterate_negative_and_remove(left_possible_operands[0], prev_left_side,
                                                                           left_potential_terms)
                    right_potential_terms = fmt.iterate_negative_and_remove(right_possible_operands[0], prev_right_side,
                                                                            right_potential_terms)
                    self.total_potential_terms = left_potential_terms + right_potential_terms
                    return_array = []
                    for term in self.total_potential_terms:
                        str = f"{term.term_coefficient}{term.term_content}"
                        return_array.append(str)
                    # print(f"Remaining Terms: {return_array}\n")

                    if len(self.total_potential_terms) <= 1:
                        return self.total_potential_terms
                    # print("\nStep 5: Remove terms in line n where related calculation is a multiplicative inverse term in line n-1")
                    # print(left_possible_operands[1], right_possible_operands[1])
                    left_potential_terms = fmt.remove_terms_from_multiplicative_inverse(left_possible_operands[1],
                                                                                        prev_left_side,
                                                                                        left_potential_terms)
                    right_potential_terms = fmt.remove_terms_from_multiplicative_inverse(right_possible_operands[1],
                                                                                         prev_right_side,
                                                                                         right_potential_terms)
                    self.total_potential_terms = left_potential_terms + right_potential_terms
                    return_array = []
                    for term in self.total_potential_terms:
                        str = f"{term.term_coefficient}{term.term_content}"
                        return_array.append(str)
                    # print(f"{return_array}\n")
                    if len(self.total_potential_terms) <= 1:
                        return self.total_potential_terms

                    simplified_left_prev, simplified_right_prev = prev_left_side.simplify_term(
                        prev_left_side), prev_right_side.simplify_term(prev_right_side)
                    if simplified_left_prev:
                        left_potential_terms = self.combinatorics_bfs(left_potential_terms, right_potential_terms,
                                                                      prev_left_side, left_side)
                        right_potential_terms = self.combinatorics_bfs(right_potential_terms, left_potential_terms,
                                                                       prev_right_side, right_side)
                    if simplified_right_prev:
                        right_potential_terms = self.combinatorics_bfs(right_potential_terms, left_potential_terms,
                                                                       prev_right_side, right_side)
                        left_potential_terms = self.combinatorics_bfs(left_potential_terms, right_potential_terms,
                                                                      prev_left_side, left_side)

                    self.total_potential_terms = left_potential_terms + right_potential_terms

                    return self.total_potential_terms

    # we pass in term line n-1 and list of potential problems and do loop
    # once called, will run through every possible combination until len(terms == 1)
    def combinatorics_bfs(self, side_potential_terms, other_potential_terms, prev_side, line_n_side):
        # put term inside the queue
        queue = deque([prev_side])
        fmt = findMistakeTerms()
        while queue:
            # prev right side is initially just line n_1 but then becomes the simplified chidlren of line n-1
            prev_side = queue.popleft()
            # now remove any right_potential_terms that are found in simplified version of prev_right_sidd
            side_potential_terms = fmt.remove_preexisting_terms(side_potential_terms, prev_side.potential_problem_terms)
            if len(side_potential_terms) + len(other_potential_terms) <= 1:
                # print("\nThere is only 1 emaining term!")
                return side_potential_terms
            simplified_terms = prev_side.simplify_term(prev_side)
            if simplified_terms:
                # print(f"\nComparing:\nLine N-1 Child: {simplified_terms[0].term_content}")
                pass
            # print(f"Line N: {line_n_side.term_content}")
            if len(simplified_terms) > 0:
                queue += simplified_terms
        return side_potential_terms

    def check_if_ones(self, array):
        return len(array) <= 1

    def print_terms_content(self):
        output_array = []
        for term in self.total_potential_terms:
            output_array.append(f"{term.term_coefficient}({term.term_content})")
        # print(f"Potential terms: {output_array}")

    # give feedback will return the line that a student messed up on
    def give_feedback(self):
        global index
        return_array = []
        for key in self.index_wrong_comparators:
            self.incorrect_indices.append(key)

        for index, term in enumerate(self.total_potential_terms, start=0):
            str = f"{term.term_coefficient}{term.term_content}"
            return_array.append(str)
        # print(f"Remaining Terms: {return_array}")
        if self.check.isCorrect:
            # print("Student is correct")
            return True
        else:
            # print(f"Student's answer {self.check.student_output}")
            # print(f"Correct answer {self.check.true_output}")
            # print(f"\nOops! Looks like you made a mistake in line {self.incorrect_line[0]+1}!")
            # print('Find your mistake on the "{}" below:')
            index = None
            clone = ""
            if self.total_potential_terms == []:
                # print("No error terms in total potential terms")
                return "No work"
            for i in range(len(self.check.text)):
                if self.incorrect_line[0] != i:
                    # print(self.check.text[i].replace(" ", ""))
                    if self.check.text[i].replace(" ", "") not in self.output_lines and i < self.incorrect_line[0] and i > 0:
                        self.output_lines.append(self.check.text[i].replace(" ", ""))
                else:  # line where term is incorrect
                    index = i
                    untouchable_index = self.untouchable.index(self.check.text[i])
                    original_ind = self.original_text.index(self.check.text[i])
                    self.incorrect_indices.append(original_ind)
                    clone = copy.deepcopy(self.check.text[i])
                    for term in self.total_potential_terms:
                        term.term_content = term.term_content.replace("x", self.check.variable)
                        new_str = f"{term.term_coefficient}{term.term_content}"
                        clone = clone.replace(" ", "").replace(new_str, "{" + new_str + "}")
                    self.untouchable[untouchable_index] = clone
            self.check.text = self.check.text[index:]
            self.reinit_check(index)
        if len(self.check.text) == 1:
            return True
            # truncate terms array

    def reinit_check(self, index):
        self.check.problem = self.check.text[0].replace(" ", "")
        self.check.isCorrect = None
        self.check.comparator = self.check.find_comparator(self.check.text[0])
        self.check.student_prob_ans = self.check.parse(self.check.problem)
        self.check.problem = self.check.student_prob_ans
        self.check.problem_left = self.check.problem.split(self.check.comparator)[0]
        self.check.problem_right = self.check.newlinesgone(self.check.problem.split(self.check.comparator)[-1])
        self.check.true_output = self.check.solve(self.check.problem_left, self.check.problem_right)
        self.check.isCorrect = self.check.verify()

    def final_feedback(self, res):
        str = ""
        if len(self.incorrect_indices) == 0 and not self.trueIsCorrect:
            # print("Work not finished. Please isolate x completely")
            str += "Work not finished. Please isolate x completely\n"
        else:
            for key in self.index_wrong_comparators:
                comp = self.index_wrong_comparators[key]
                self.untouchable[key] = self.untouchable[key].replace(comp, "{" + comp + "}")
            self.trueIsCorrect = self.trueIsCorrect and self.index_wrong_comparators == {}
            if self.trueIsCorrect and len(self.index_wrong_comparators) == 0:
                # print("Student is correct")
                str += "Student is correct\n"
            else:
                # print(f"Student's answer {self.check.student_output}")
                # print(f"Correct answer {self.check.true_output}")
                st = ""
                self.incorrect_indices = list(set(self.incorrect_indices))
                if len(self.incorrect_indices) > 1:
                    for i in range(len(self.incorrect_indices) - 1):
                        st += f"{self.incorrect_indices[i] + 1}, "
                    st += f"and {self.incorrect_indices[len(self.incorrect_indices) - 1] + 1}"
                    # print(f"Oops! Looks like you made a mistake in lines: {st}!")
                    # print('Find your mistakes on the "{}" below:\n')
                    str += f"Oops! Looks like you made a mistake in lines: {st}!\n"
                    str += 'Find your mistakes on the "{}" below:\n'
                else:
                    st += f"{self.incorrect_indices[0] + 1}"
                    # print(f"Oops! Looks like you made a mistake in line: {st}!")
                    str += f"Oops! Looks like you made a mistake in line: {st}!\n"
        for line in self.untouchable:
            # print(line)
            str += f"{line}\n"
        return str

    # loop until done (text only has one line left)
    def main(self):
        global res
        while len(self.check.text) > 1:
            # print(self.check.text)
            # check if
            self.check_consistent_comparators()
            self.find_mistake_terms()
            res = self.give_feedback()
            if res or res == "No work":
                break
            # print("\n\n\n")
        str = self.final_feedback(res)
        output_json = {"solver": str}
        print(output_json)
        return output_json
