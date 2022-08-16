import json_form

#  works perfectly
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


# passes
# dict = {
#
#     "1": "2v + 18 = 16 - 4(v + 7)",
#
#     "2": "2v + 18 = 16 - 4v + -28",
#
#     "3": "2v + 18 + 12 = -12 - 4v + 12",
#
#     "4": "2v + 30 - 2v = -4v - 2v",
#
#     "5": "30 = -6v",
#
#     "6": "v = 5"
#
# }

# passes
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
#     "5": "6v = -30",
#
#     "6": "v = -5"
#
# }
# jake is ok with this
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

# looking at first mistake, i'm CORRECT!!!
# jake highlighted 15 in line 4, but it should be -3x in line 2?? for first mistake
# dict = {
#
#     "1": "4x – (9 – 3x) = 8x - 1",
#
#     "2": "4x – 9 – 3x + 4 = 8x – 1 + 4",
#
#     "3": "7x – 9 + 8 = 8x – 1 = 8",
#
#     "4": "15x – 9 + 9 = -1 + 9",
#
#     "5": "15x/15 = 10/15",
#
#     "6": "1.5"
#
# }


# WORKS PERFECTLY
# dict = {
#
#     "1": "12(3+1y) = 5(2y+8)",
#
#     "2": "36+1y-36 = 10y+40-36",
#
#     "3": "1y-10y = 10y+4-10y",
#
#     "4": "-9y = 4",
#
#     "5": "y = -0.44"
#
# }
#  CORRECT
# dict = {
#
#     "1": "-7(1-4m) = 13(2m-3)",
#
#     "2": "-7+28m-26m = 26m-39-26m",
#
#     "3": "-7+2m+7 = -39+7",
#
#     "4": "2m = -46",
#
#     "5": "m = -23"
#
# }
# PERFECT! jake highlights -7 in line 2 but should be -28 in line 2
# dict = {
#
#     "1": "-7(1-4m) = 13(2m-3)",
#
#     "2": "-7-28m+7 = 26m-39+7",
#
#     "3": "-28m = 26m-32-26m",
#
#     "4": "-54 = -32",
#
#     "5": "0.592"
#
# }


#  jake highlighted the -45 on right side of line 4 but it should be the -60 in line 5 in right side
# WORKS WELL!!
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
# PERFECT
# dict = {
#
#     "1": "4x+5(7x-3) = 9(x-5)",
#
#     "2": "4x+35-15 = 9(x-5)",
#
#     "3": "4x+35-15 = 9x-45",
#
#     "4": "4x+20-4x = 9x-45-4x",
#
#     "5": "20+45 = 5x-45+45",
#
#     "6": "65/5 = 5x/5",
#
#     "7": "x = 13"
#
# }
# PERFECT
# dict = {
#
#     "1": "2(6d+3) > 18-3(16-3d)",
#
#     "2": "12d+3 < 18-48+9d",
#
#     "3": "12d+3-9d > -30+9d-9d",
#
#     "4": "3d+3-3 > 30-3",
#
#     "5": "3d > -33",
#
#     "6": "d > -11"
#
# }
#  PASSING
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
#  PERFECT
# dict = {
#
#     "1": "8(4u-1)-12u = 11(2u-6)",
#
#     "2": "24u-8-12u = 22u-66",
#
#     "3": "12u-8+8 = 22u-66+8",
#
#     "4": "12u = 22u-58-22u",
#
#     "5": "10u = 58",
#
#     "6": "u = 5 4/5"
#
# }




# PERFECT
# dict = {
#
#     "1": "8(4u-1)-12u = 11(2u-6)",
#
#     "2": "32u-8-12u+22 = 22u-66+22",
#
#     "3": "32u-34u+32 = 66+32",
#
#     "4": "34u/34 = 98/34 = 2 15/17"
#
# }
# #
# dict = {
#
#     "1": "-5-(15y-1)  = 2(7y-16)-y",
#
#     "2": "5-15y-1+1 = 14y-32-1y+1",
#
#     "3": "-15y-1+15 = 15y – 32 + 15",
#
#     "4": "-5-30y-1+1 = 32+1",
#
#     "5": "-4-30y-4 = 32-4",
#
#     "6": "30y/30 = 28/30 = 14/15"
#
# }




#  Think jake made a mistake because -16t is just randomly thrown in on line 2, but he highlights 14t
# dict = {
#
#     "1": "+8(2t - 6) = 2 + 14t",
#
#     "2": "+16t - 48 - 16t = 2 + 14t",
#
#     "3": "-48 = 2 + 14t – 14t",
#
#     "4": "-27t + -48 - 48 = 2 - 48",
#
#     "5": "-27t/-27 = -46/-27"
#
# }


# #  Pretty carzy edge case where change two term values
#
# dict = {
#
#     "1": "2(12 – 8x) – x = x – 11x - x",
#
#     "2": "23 – 16x + 16 = -11x + 16",
#
#     "3": "23/23 = 5/23"
#
# }

#*FIX THIS THIS IS REALLY BAD*

# dict = {
#
#     "1": "2v + 18 = 16 – 4(v + 7)",
#
#     "2": "2v/-4v + 18 = 16 -4v/-4v - 28",
#
#     "3": "-2v + 18 + 28 = 16 – 28 + 28",
#
#     "4": "26v + 18 – 18 = 16 - 18",
#
#     "5": "26v/26 = -2/26"
#
# }

# my output is valid in that in line 3, left -99 and right 99 shoudn't be there
# dict = {
#
#     "1": "9(11-k) = 3(3k-9)",
#
#     "2": "99-9k-9 = 9k-27-9",
#
#     "3": "-18k-99+99 = -27+99",
#
#     "4": "-18k/18 = 72/18 = 4"
#
# }

#
# dict = {
#     "1": "9(11-k) > 4(3k-9)",
#     "2": "99+9k > 12k-27",
#     "3": "127 > 3k",
#     "4": "k > 100"
# }
#
# dict = {
#     "1": "2x>3+23",
#     "2": "2x<25",
#     "3": "x<3"
# }
# 2x>3+23
# 2x{<}{25}
# x<{13}
#
#  is correct
# dict = {
#     "1": "-2x<26",
#     "2": "x>-12"
# }
# -2x<26  expected output
# x>{-12}

dict = {
    "1": "3x+1 > 4",
    "2": "3x+1<4"
}


# expected:
#   "2: "-2x>40"
#   "3: "x<-20

# dict = {
#     "1": "-2x+4x+3=41",
#     "2": "2x+3=42",
#     "3": "2x=39",
#     "4": "x=19"
# }

# a line could be wrong because the inflection point is wrong (already done)
# or the line could be wrong because the comparator is wrong
#if you plug in the inflection point
    # put in the inflection point # this is if the answer is right or wrong
    # then put in 1% greater
    # then put in 1% less

    # these three things ideally should be the same across the entire equation