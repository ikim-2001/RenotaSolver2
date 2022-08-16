
# works
# dict = {
#     "1": "3x+1 > 4",
#     "2": "3x+1<4"
# }

# # works
# dict = {
#     "1": "3x+1 > 4",
#     "2": "-3x+1<4"
# }
#
# # works
global dict
dict = {
    "1": "3x+1 > 2",
    "2": "-3x+1>1"
}
def print_dict(str):
    print(str)



# works
# dict = {
#     "1": "3x+1 > 4",
#     "2": "6x+1>4",
#     "3": "6x>3",
#     "4": "x<2"
# }

# works

# dict = {
#     "1": "-3(x+10) > 3",
#     "2": "-3x-30>3",
#     "3": "x>-11"  # should be incorrect
# }

# if line is last line, if inflections same but triple bool diff, mark the thing

# if triple boolean same, don't highlight comparator
#


# thing we talked about using the booleans (is it the right direction)
# if it's the same exact character, then we don't wanna penalize a student for transposing something from line before
# if the inflection point is correct but not comparator
# if the comparator is the only thing wrong, then it's the only thing before

# works
# dict = {
#     "1": "-24x<408",
#     "2": "3x<-2"
# }

#
# dict = {
#     "0": "-24x<44+4",
#     "1": "-24x<48",
#     "2": "x>-3"
# }

# dict = {
#     "1": "-3x+1>4",
#     "2": "-3x+2>7",
#     "3": "x<6"
# }
# great
# dict = {
#
#     "1": "2(12 - 8x) = x - 11x",
#
#     "2": "24  -16x + 1 = x - 11x + 1",
#
#     "3": "24 - 17x + 17 = 12x + 17",
#
#     "4": "24/29 = 29x/29 = 24/29"
#
# }

# great
# dict = {
#     "1": "9(11-x) > 4(3x-9)",
#     "2": "99-9x > 12x-27",
#     "3": "126 < 3x",
#     "4": "x > 42"
# }

# dict = {
#
#     "1": "2(6d+3) = 18-3(16-3d)",
#
#     "2": "12d+6+9 = 18-48-9d+9",
#
#     "3": "21d+6+18 = 18-48+18",
#
#     "4": "21d+6-6 = 66-6",
#
#     "5": "21d/21 = 60/21",
#
#     "6": "= 2 6/7"
#
# }

# dict = {
#
#     "1": "2v + 18 = 16 - 4(1v + 7)",
#
#     "2": "2v + 18 + 4v = 16 - 4v - 28 + 4v",
#
#     "3": "6v + 18 + 28 = 16 - 28 + 28",
#
#     "4": "6v + 46 - 46 = 16 - 46",
#
#     "5": "6v = -21",
#
#     "6": "v = 3"
#
# }
# dict = {
#     "1": "2x + 3 =4",
#     "2": "2x = 3"
# }

# dict = {
#
#     "1": "2v + 18 = 16 - 4(v + 7)",
#
#     "2": "2v + 18 + 4 = 16 - 4v + 28 + 4",
#
#     "3": "6v + 18 - 16 = 16 + 28 - 16",
#
#     "4": "6v + 18 - 18 = 28 - 18",
#
#     "5": "6v/6 = 10/6 = 1 2/3"
#
# }

# dict = {
#
#     "1": "12(3+1y) = 5(2y+8)",
#
#     "2": "36+1y-36 = 10y+40-36",
#
#     "3": "1y-10y = 10y+4-10y",
#
#     "4": "-8y = 4",
#
#     "5": "y = -0.44"
#
# }
#
# dict = {
#
#     "1": "4x+5(7x-3) = 9(x-5)",
#
#     "2": "4x+35x-15 = 9x-45",
#
#     "3": "39x-15-9x = 9x-45-9x",
#
#     "4": "30x-15+15 = -45+15",
#
#     "5": "30x = -60",
#
#     "6": "x = -2"
#
# }