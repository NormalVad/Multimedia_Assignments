import math

## LZW

def lzw_encoding(s):
    # s is the string to be encoded
    dictionary = {};
    dictionary['a'] = 0
    dictionary['b'] = 1
    dictionary['r'] = 2
    dictionary['y'] = 3
    dictionary['.'] = 4

    current_code = 5



    encoded_code = []

    previous = s[0]
    current = ""

    for i in range(len(s)):
        if (i != len(s) - 1):
            current = current + s[i + 1]
        tem = previous + current
        if (tem in dictionary):
            previous = tem
        else:
            encoded_code.append(dictionary[previous])
            dictionary[tem] = current_code
            current_code = current_code + 1
            previous = current
        current = ""

    encoded_code.append(dictionary[previous])
    print(dictionary)
    print("Encoded Code is :")
    print(encoded_code)
    return encoded_code;


print("Hello")

lzw_encoding("ababbabababba")


