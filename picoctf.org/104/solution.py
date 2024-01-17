#!/bin/python3 

# ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])


# the algorithm:
# iterates through pairs of letters
# shifts the first letter left by one byte and adds the value of the next character

str = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸弲㘶㠴挲ぽ"
flag = ""

for i in range(len(str)):
    # we know the flag is ascii (characters are 1 byte) so we don't need to worry about the addition and can just undo the shift to get the first character
    c1 = chr(ord(str[i]) >> 8)
    c2 = chr(ord(str[i]) % 256)
    flag = flag + c1 + c2

print(flag)
