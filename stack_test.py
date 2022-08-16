from Checker import *
from main import *

dict = {
    "0": "-8x+2 < -3(2x-6)",
    "1": "-8x+2 < -6x-18",
    "2": "-2x+2 < -18"
}
# instance = Checker(dict)
main = Main(dict)
print(main.main())