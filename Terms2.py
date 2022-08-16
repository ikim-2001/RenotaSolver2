import collections
import copy
from Checker import *
from string import ascii_uppercase
alphabet = list(ascii_uppercase)*10000
class Term:
    def __init__(self, _term_coefficient, _input_string, inflectiondict, greaterdict, lesserdict, _constants_vars_dict, _input_stack_level):
        # self.potential_problems = _input_potential_problems
        # self.input_string_lookup_dict = _input_string_lookup_dict
        self.input_string_lookup_dict = inflectiondict
        self.input_string_lookup_dict_greater = greaterdict
        self.input_string_lookup_dict_lesser = lesserdict
        # initilaized as 1 when creating new term
        self.term_coefficient = _term_coefficient
        self.term_content = _input_string
        self.parsed_list = self.parse_subterms(_input_string)
        # recursively incremented with each new child term class
        self.input_stack_level = _input_stack_level
        self.constants_vars_dict = _constants_vars_dict
        self.check = check
        if self.term_content != "x" and self.term_coefficient != "":
            self.child_terms = self.classify_terms(self.parsed_list)
        else:
            self.child_terms = []
        # helps in inputting into the potential error terms array, if base, then just add normally, else, if nested,
        # create a brand new term where coeff = coeff of nested and content = "". Then have that term's associativity as the parent term's
        # associativity. This will tell whether or not we should take it out
        self.nested_or_base = self.determine_type_term()
        # list of 1, x, or both
        self.xs_ones_both = self.determine_associated_type()
        self.potential_problem_terms = self.determine_potential_terms()
        self.id = None
        self.affiliated_coeff = None
        self.is_lone_coeff_term = False
        self.display_potental_terms = []
        for i in range(len(self.potential_problem_terms)):
            self.display_potental_terms.append(f"{self.potential_problem_terms[i].term_coefficient}{self.potential_problem_terms[i].term_content}")
        for term in self.potential_problem_terms:
            term.id = alphabet.pop(0)

    def get_coef(self):
        return self.term_coefficient
    def get_content(self):
        return self.term_content
    def get_stack_level(self):
        return self.input_stack_level
    def get_id(self):
        return self.id
    # def get_association(self):
    #     return


    # takes in string, returns either:
    # nested or base
    def determine_type_term(self):
        # first verify that term has no kids??
        if len(self.child_terms) == 0:
            return "base"
        return "nested"

    # if base return 1s or xs
    # if nested, return affiliated with x's, 1's or both
    def determine_associated_type(self):
        list_of_types = []
        if self.nested_or_base == "base":
            if "x" in self.term_content:
                list_of_types.append("x")
                return list_of_types
            else:
                list_of_types.append("1")
                return list_of_types
        # case in which is nested
        else: # 2(x-1)
            for child in self.child_terms:
                if child.nested_or_base == "base":
                    if child.determine_associated_type() == ["x"]:
                        if "x" not in list_of_types:
                            list_of_types.append("x")
                    # basic and ones
                    else:
                        if "1" not in list_of_types:
                            list_of_types.append("1")
                        continue
                # child is nested
                else:
                    list_of_types = child.determine_associated_type()
            return list_of_types

    def parse_subterms(self, input_string):
        stack = []
        substrings = []
        coefficients = []
        curr_substring = ""
        curr_coeff_substring = ""
        curr_coeff = 1
        if input_string == "":
            return substrings
        for i in range(len(input_string)):
            if input_string[i] == "(":
                if len(stack) > 0:
                    curr_substring += input_string[i]
                stack.append("(")
            elif len(stack) > 0 and input_string[i] != ")":
                curr_substring += input_string[i]
            elif input_string[i] == ")":
                stack.pop()
                if len(stack) == 0:
                    substrings.append((curr_coeff_substring, curr_substring))
                    curr_substring = ""
                    curr_coeff_substring = ""
                else:
                    curr_substring += input_string[i]
            elif input_string[i] in ["+", "-"] and len(stack) == 0:
                substrings.append((curr_coeff_substring, curr_substring))
                # refresh the curr_substring so new term
                curr_substring, curr_coeff_substring = "", ""
                curr_coeff_substring += input_string[i]
            elif len(curr_coeff_substring) >= 0 and (len(stack) == 0 and (input_string[i] in [".", "/"] or input_string[i].isnumeric())):
                curr_coeff_substring += input_string[i]
                if i == len(input_string)-1:
                    substrings.append((curr_coeff_substring, curr_substring))
            elif not input_string[i].isnumeric():
                curr_substring += input_string[i]
                if i == len(input_string)-1:
                    substrings.append((curr_coeff_substring, curr_substring))

        return substrings

    def classify_terms(self, list_of_coeffs_and_terms):
        classified_term_list = []
        # if the term consists of multiple terms
        # t)
        for i in range(len(list_of_coeffs_and_terms)):
            coef, content = list_of_coeffs_and_terms[i][0], list_of_coeffs_and_terms[i][1]
            if coef == "+" and content == "":
                continue
            elif coef == "" and content == "":
                continue
            # elif coef != "" and content == "":
            #     continue
            elif coef == "" or coef == "+":
                coef = "1"
            elif coef == "-":
                coef = "-1"
            classified_term = Term(eval(coef), content, self.input_string_lookup_dict, self.input_string_lookup_dict_greater,
            self.input_string_lookup_dict_lesser, self.constants_vars_dict, self.input_stack_level + 1)
            classified_term_list.append(classified_term)
        return classified_term_list

    def evaluate(self):
        if len(self.child_terms) > 0:
            stored_total = 0
            for term in self.child_terms:
                stored_total += self.term_coefficient*term.evaluate()
            return stored_total
        else:
            return self.term_coefficient*self.input_string_lookup_dict[self.term_content]

    def toggle(self, upperlower):
        if len(self.child_terms) > 0:
            stored_total = 0
            for term in self.child_terms:
                stored_total += self.term_coefficient*term.toggle(upperlower)
            return stored_total
        else:
            if upperlower == "upper":
                # upperlower is either upper or lower in the key
                return self.term_coefficient*self.input_string_lookup_dict_greater[self.term_content]
            return self.term_coefficient*self.input_string_lookup_dict_lesser[self.term_content]

    def determine_potential_terms(self):
        potential_terms = []
        curr_coef = None
        for term in self.child_terms:
            if term.nested_or_base == "base":
                potential_terms.append(term)
            # term is nested
            else:
                # append the coeff as a new term
                # then break down the chidren terms inside the nest and add them to the array
                coef_term = Term(term.term_coefficient, "", self.input_string_lookup_dict, self.input_string_lookup_dict_greater,
                                 self.input_string_lookup_dict_lesser, self.constants_vars_dict, self.input_stack_level)
                # set coeff to have affiliation with interior nested children's type
                coef_term.xs_ones_both = self.xs_ones_both
                # set the coeff term to have this status flipped on
                coef_term.is_lone_coeff_term = True
                potential_terms.append(coef_term)
                # potential terms of the coeff (when nested)
                det_pot_terms = term.determine_potential_terms()
                for i in range(len(det_pot_terms)):
                    if not det_pot_terms[i].affiliated_coeff:
                        det_pot_terms[i].affiliated_coeff = term.term_coefficient
                potential_terms += det_pot_terms
        # if type is x and 1, then coeff
        # for term in potential_terms:
        #     if term.xs_ones_both
        for term in potential_terms:
            if ["x", "1"] == term.xs_ones_both:
                term.affiliated_coeff = None
        return potential_terms


    def cons_var_eval(self):
        if len(self.child_terms) == 0:
            if self.term_content == "x":
                return (0, self.term_coefficient)
            elif self.term_content == "":
                return (self.term_coefficient, 0)
        else:
            for child in self.child_terms:
                # print(f"{child.term_coefficient}({child.term_content} is a child)")
                # print(f"{child.term_coefficient}({child.term_content}) {child.term_content == ''}")
                self.constants_vars_dict["1's"] += self.term_coefficient*child.cons_var_eval()[0]
                self.constants_vars_dict["x's"] += self.term_coefficient*child.cons_var_eval()[1]
            return (0, 0)


    def simplify_term(self, input_term):
        simplified_fixed_terms = []
        simplified_broken_terms = self.combinatorics_distribute_coeffs(input_term) + self.combinatorics_add_like_terms(input_term)
        fixed_terms = self.reconstruct_broken_to_fixed(simplified_broken_terms)
        # print(f"{input_term.term_content} => {fixed_terms}")
        for term in fixed_terms:
            new_term = Term(1, term, {"x": eval(self.check.true_output), "": 1}, {"x": eval(self.check.true_output)*2, "": 1},
                            {"x": eval(self.check.true_output)/2, "": 1}, {"1's": 0, "x's": 0}, 0)
            simplified_fixed_terms.append(new_term)
        return simplified_fixed_terms

    def reconstruct_broken_to_fixed(self, array):
        # takes in an array full of lists that consist of subterms
        unified_terms_list = []
        for broken_term_list in array:
            substring = ""
            stack = []
            for i in range(len(broken_term_list)):
                if i > 0:
                    if broken_term_list[i - 1].input_stack_level < broken_term_list[i].input_stack_level:
                        substring += f"({self.reconstruct_string(broken_term_list[i])}"
                        stack.append("(")
                    elif broken_term_list[i - 1].input_stack_level > broken_term_list[i].input_stack_level and \
                            broken_term_list[i - 1].input_stack_level > 1:
                        substring += f"){self.reconstruct_string(broken_term_list[i])}"
                        stack.pop()
                    else:
                        substring += self.reconstruct_string(broken_term_list[i])
                else:
                    substring += self.reconstruct_string(broken_term_list[i])
            if stack:
                substring += ")"
            unified_terms_list.append(substring)
        return unified_terms_list

    def reconstruct_string(self, term):
        if term.term_coefficient > 0:
            return f"+{term.term_coefficient}{term.term_content}"
        return f"{term.term_coefficient}{term.term_content}"

    

    def combinatorics_distribute_coeffs(self, input_term):
        simplified_terms = []
        nested = []
        for term in input_term.potential_problem_terms:
            if term.is_lone_coeff_term:
                nested.append(term)
        for i in range(len(nested)):
            input_potential_problem_terms = copy.deepcopy(input_term).potential_problem_terms
            ids = list(map(Term.get_id, input_potential_problem_terms))
            for term in input_potential_problem_terms:
                # if affiliated coeff matches the coef in nested list
                if term.affiliated_coeff == nested[i].term_coefficient:
                    term.term_coefficient *= term.affiliated_coeff
                    term.affiliated_coeff = None
                    term.input_stack_level -= 1
            if nested[i].id in ids:
                index = ids.index(nested[i].id)
                input_potential_problem_terms.pop(index)
            simplified_terms.append(input_potential_problem_terms)
        # for lst in simplified_terms:
        #     print(f"\nDistributing in {input_term.term_content}:")
        #     for term in lst:
        #         print(f"child: {term.term_coefficient}({term.term_content}) Level: {term.input_stack_level} type: {term.xs_ones_both} aff: {term.affiliated_coeff}")
        #     print("")

        return simplified_terms


    def combinatorics_add_like_terms(self, input_term):
        simplified_terms = []
        for i in range(len(input_term.potential_problem_terms)):
            for j in range(i, len(input_term.potential_problem_terms)):
                pot_terms = copy.deepcopy(input_term).potential_problem_terms
                ids = list(map(Term.get_id, pot_terms))
                # so that it's a unique combo
                if j > i:
                    # if both are x's
                    if pot_terms[i].xs_ones_both == pot_terms[j].xs_ones_both and pot_terms[i].affiliated_coeff == pot_terms[j].affiliated_coeff:
                        if pot_terms[i].input_stack_level == pot_terms[j].input_stack_level and not pot_terms[i].is_lone_coeff_term:
                            new_term_coeff = new_term_coeff = pot_terms[i].term_coefficient + pot_terms[j].term_coefficient
                            new_term_content = "x" if pot_terms[i].xs_ones_both == ["x"] else ""
                            added_term = Term(new_term_coeff, new_term_content,{"x": eval(self.check.true_output), "": 1}, {"x": eval(self.check.true_output)*2, "": 1}, {"x": eval(self.check.true_output)/2, "": 1}, {"1's": 0, "x's": 0}, pot_terms[i].input_stack_level)
                            # replace i with new term and pop j!!
                            pot_terms[i] = added_term
                            j_ind = self.search_for_id_term(pot_terms[j].id, pot_terms)
                            pot_terms.pop(j_ind)
                            simplified_terms.append(pot_terms)

        return simplified_terms

    def bfs_display(self):
        queue = collections.deque(self.simplify_term(self))
        count = 0
        print("Input:")
        print(self.term_content)
        print("")
        seen = []
        while queue:
            curr = queue.popleft()
            if curr.term_content not in seen:
                curr_children = curr.simplify_term(curr)
                count += 1
                print(curr.term_content)
                if curr_children:
                    queue += curr_children
        print(count)

    # takes in an array and a unique id, scours for that id and returns that term's index (used later for pop)
    def search_for_id_term(self, id, array):
        for term in array:
            if id == term.id:
                return array.index(term)

    # term1 !!!!!! term2


