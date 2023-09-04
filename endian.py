import numpy as np
from itertools import permutations

hex_vals = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
char_vals = [i+j for (i, j) in list(permutations(hex_vals, 2))]
char_vals

for i in range(100):
    integer32 = np.random.choice(char_vals, 4)
    string_1, string_2 = "0x", "0x"
    for (byte_1, byte_2) in zip(integer32, np.flip(integer32)):
        string_1 += byte_1
        string_2 += byte_2
    print(f"BE2LE_U32({string_1}) == {string_2} &&")
    

for i in range(100):
    integer32 = np.random.choice(char_vals, 8)
    string_1, string_2 = "0x", "0x"
    for (byte_1, byte_2) in zip(integer32, np.flip(integer32)):
        string_1 += byte_1
        string_2 += byte_2
    print(f"BE2LE_U64({string_1}) == {string_2} &&")