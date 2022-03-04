import math
from PIL import Image
import os

# LZW

def lzw_encoding_binary(s):
    # s is the string to be encoded
    binary_string = ""
    dictionary = {};
    dictionary['0'] = 0
    dictionary['1'] = 1

    current_code = 2

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
            binary_string = binary_string + str(dictionary[previous])
            dictionary[tem] = current_code
            current_code = current_code + 1
            previous = current
        current = ""

    encoded_code.append(dictionary[previous])
    binary_string = binary_string + str(dictionary[previous])
    return binary_string;

# for converting integer to binary
def convert_to_binary(n):
    return bin(n)[2:].zfill(8)



def image_to_binary (address):
    img = Image.open(address)
    width, height = img.size

    binary_string = ""

    print("Width and Height of Image : ", width," , ",height)

    pixel = img.load()
    for x in range(width):
        for y in range(height):
            tem = pixel[x, y]
            red = convert_to_binary(tem[0])
            green = convert_to_binary(tem[1])
            blue = convert_to_binary(tem[2])
            # print(red,blue,green)
            binary_string = binary_string + red;
            binary_string = binary_string + green;
            binary_string = binary_string + blue;

    return binary_string

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


# Experiment 1
lzw_encoding("a.bar.array.by.barrayar.bay")

address = "D:\IITD\SEMESTER 6\ELL786\sample.bmp"
size_of_image = os.path.getsize(address)*8
bmp_to_binary = image_to_binary(address)
print("Length of Binary String = ",len(bmp_to_binary))
lzw_coded_string = lzw_encoding_binary(bmp_to_binary)
print("Length_of_lzw_string = ",len(lzw_coded_string))
lzw_compression = ((size_of_image - len(lzw_coded_string))/size_of_image)*100
print(lzw_compression," %")


# Experiment 2 : GIF image
print("Part : 2")
address = "D:\IITD\SEMESTER 6\ELL786\sample.bmp"
size_of_image = os.path.getsize(address)
print("Size of Image is : ", size_of_image)

img = Image.open(address)
img.save("gif_ell786_image.gif")

size_of_compressed_image = os.path.getsize("gif_ell786_image.gif")
print("Size of GIF image is : " , size_of_compressed_image)

print(((size_of_image-size_of_compressed_image)/size_of_image)*100,"%")

print("Compression Ratio = ", size_of_image/size_of_compressed_image)


# Experiment 3 : PNG image
print("Part : 3")
address = "D:\IITD\SEMESTER 6\ELL786\sample.bmp"
size_of_image = os.path.getsize(address)
print("Size of Image is : ", size_of_image)

img = Image.open(address)
img.save("png_ell786_image.png")

size_of_compressed_image = os.path.getsize("png_ell786_image.png")
print("Size of PNG image is : " , size_of_compressed_image)

print(((size_of_image-size_of_compressed_image)/size_of_image)*100,"%")
print("Compression Ratio = ", size_of_image/size_of_compressed_image)
