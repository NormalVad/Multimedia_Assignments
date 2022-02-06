import random
import math

def toBinary(a):
    res = ''.join(format(ord(i), '07b') for i in a)
    return res

def toString(a):
    k = len(a)
    res = ""
    for i in range(0,k,7):
        temp = a[i:i+7]
        val = int(temp,2)
        res += chr(val)
    return res

def random_bin_pattern(M,d):
    t = int(M/d)
    r = random.randrange(1,t+1)
    ran_pattern = ""
    for i in range(M):
        if((i-r+1)%t == 0):
            ran_pattern += '1'
        else:
            ran_pattern += '0'
    return ran_pattern

def xoring(a,b):
    k = len(a)
    res = ""
    for i in range(k):
        if(a[i] == b[i]):
            res += '0'
        else:
            res += '1'
    return res

def process_wo_decoding(M,bin_input,input_file):
	d_arr = [10,100,200,500,5000]
	# d_arr = [10]
	modi_percent_arr = []
	for d in d_arr:
		ran_pattern = random_bin_pattern(M,d)
		y = xoring(bin_input,ran_pattern)
		y_text = toString(y)
		count = 0
		length_inp = len(input_file)
		for i in range(length_inp):
			if(input_file[i] != y_text[i]):
				count += 1
		modi_percent = float(count*100)/length_inp
		modi_percent_arr.append(modi_percent)
	for i in range(len(modi_percent_arr)):
		print('d = ' + str(d_arr[i]) + ', modified_percentage = ' +str(modi_percent_arr[i]))

def huff_decoding(y,huff_chunk_tree,huff_chunk_len):
	res = ""
	num_chunks = len(huff_chunk_len)
	length = 0
	for i in range(num_chunks):
		chunk = y[length:length+huff_chunk_len[i]]
		length += huff_chunk_len[i]
		# print(chunk)
		node = huff_chunk_tree[i]
		for j in chunk:
			if(j == '0'):
				node = node.left
			else:
				node = node.right
			if(not node.left and not node.right):
				res += node.symbol
				node = huff_chunk_tree[i]
		# print(len(res))
	return res

def process_w_decoding(M,bin_input,input_file,huff_chunk_tree,huff_chunk_len):
	d_arr = [10,100,200,500,5000]
	# d_arr = [10]
	modi_percent_arr = []
	for d in d_arr:
		ran_pattern = random_bin_pattern(M,d)
		y = xoring(bin_input,ran_pattern)
		y_text = huff_decoding(y,huff_chunk_tree,huff_chunk_len)
		y_text = toString(y_text)
		# print(str(len(y_text)))
		# print(str(len(input_file)))
		count = 0
		length_inp = len(input_file)
		for i in range(length_inp):
			if(input_file[i] != y_text[i]):
				count += 1
		modi_percent = float(count*100)/length_inp
		modi_percent_arr.append(modi_percent)
		# if(d == 10):
		# 	print('inp: ' + str(input_file) + "\n")
		# 	print('output: ' + str(y_text))

	for i in range(len(modi_percent_arr)):
		print('d = ' + str(d_arr[i]) + ', modified_percentage = ' +str(modi_percent_arr[i]))

# A Huffman Tree Node
class node:
	def __init__(self, freq, symbol, left=None, right=None):
		# frequency of symbol
		self.freq = freq

		# symbol name (character)
		self.symbol = symbol

		# node left of current node
		self.left = left

		# node right of current node
		self.right = right

		# tree direction (0/1)
		self.huff = ''

# utility function to print huffman
# codes for all symbols in the newly
# created Huffman tree

def extractNodes(a, node, val=''):
	# huffman code for current node
	newVal = val + str(node.huff)

	# if node is not an edge node
	# then traverse inside it
	if(node.left):
		extractNodes(a,node.left, newVal)
	if(node.right):
		extractNodes(a,node.right, newVal)

	# if node is edge node then
	# display its huffman code
	if(not node.left and not node.right):
		# print(f"{node.symbol} -> {newVal}")
		a[node.symbol] = newVal


## Part 1 Exp-1
input_file = open("ASSN1.txt", "r").read()
bin_input = toBinary(input_file)
M = len(bin_input)
process_wo_decoding(M,bin_input,input_file)
     
## Part 1 Exp - 2  HUFFMAN
num_chunks = 7
k = int(M/num_chunks)
huff_inp = ""
huff_chunk_tree = []
huff_chunk_len = []

for i in range(num_chunks):
	chunk = bin_input[i*k:(i+1)*k]
	num_zeros,num_ones = 0,0
	for j in chunk:
		if(j == '0'):
			num_zeros += 1
		else:
			num_ones += 1

	# characters for huffman tree
	chars = ['0','1']

	# frequency of characters
	freq = [ num_zeros, num_ones]

	# list containing unused nodes
	nodes = []

	# converting characters and frequencies
	# into huffman tree nodes
	for x in range(len(chars)):
		nodes.append(node(freq[x], chars[x]))

	while len(nodes) > 1:
		# sort all the nodes in ascending order
		# based on their frequency
		nodes = sorted(nodes, key=lambda x: x.freq)

		# pick 2 smallest nodes
		left = nodes[0]
		right = nodes[1]

		# assign directional value to these nodes
		left.huff = 0
		right.huff = 1

		# combine the 2 smallest nodes to create
		# new node as their parent
		newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)

		# remove the 2 nodes and add their
		# parent as new node among others
		nodes.remove(left)
		nodes.remove(right)
		nodes.append(newNode)

	huff_chunk_tree.append(nodes[0])

	huff_code = {}

	# Huffman Tree is ready!
	extractNodes(huff_code, nodes[0])


	huff_chunk = ""
	for t in chunk:
		huff_chunk += huff_code[t]
	huff_chunk_len.append(len(huff_chunk))
	huff_inp += huff_chunk

M_huff = len(huff_inp)
process_w_decoding(M_huff,huff_inp,input_file,huff_chunk_tree,huff_chunk_len)

## EXTENDED HUFFMAN
huff_inp1 = ""
huff_chunk_tree1 = []
huff_chunk_len1 = []

for i in range(num_chunks):
	chunk = bin_input[i*k:(i+1)*k]
	# Frequency of Characters
	freq = {
		'0000': 0,
		'0001': 0,
		'0010': 0,
		'0011': 0,
		'0100': 0,
		'0101': 0,
		'0110': 0,
		'0111': 0,
		'1000': 0,
		'1001': 0,
		'1010': 0,
		'1011': 0,
		'1100': 0,
		'1101': 0,
		'1110': 0,
		'1111': 0,
	}
	# characters for huffman tree
	# chars = ['0000','0001', '0010','0011','0100','0101','0110','0111','1000','1001', '1010','1011','1100','1101','1110','1111']
	
	for i in range(0,M,4):
		tmp = str(bin_input[i:i+4])
		freq[tmp] += 1
	
	# list containing unused nodes
	nodes = []

	# converting characters and frequencies
	# into huffman tree nodes
	for x,y in freq.items():
		nodes.append(node(y, x))

	while len(nodes) > 1:
		# sort all the nodes in ascending order
		# based on their frequency
		nodes = sorted(nodes, key=lambda x: x.freq)

		# pick 2 smallest nodes
		left = nodes[0]
		right = nodes[1]

		# assign directional value to these nodes
		left.huff = 0
		right.huff = 1

		# combine the 2 smallest nodes to create
		# new node as their parent
		newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)

		# remove the 2 nodes and add their
		# parent as new node among others
		nodes.remove(left)
		nodes.remove(right)
		nodes.append(newNode)

	huff_chunk_tree1.append(nodes[0])

	huff_code = {}

	# Huffman Tree is ready!
	extractNodes(huff_code, nodes[0])


	huff_chunk = ""
	for t in range(0,k,4):
		t1 = chunk[t:t+4]
		huff_chunk += huff_code[t1]
	huff_chunk_len1.append(len(huff_chunk))
	huff_inp1 += huff_chunk

M_huff1 = len(huff_inp1)
process_w_decoding(M_huff1,huff_inp1,input_file,huff_chunk_tree1,huff_chunk_len1)



# Arithmetic


def to_bin(number, places):
    whole, dec = str(number).split(".")
  
    whole = int(whole)
    dec = int (dec)

    res = bin(whole).lstrip("0b") + "."
    
    for x in range(places):
        whole, dec = str((to_decimal(dec)) * 2).split(".")
        dec = int(dec)
        res += whole
    return res
  
def to_decimal(num): 
    while num > 1:
        num /= 10
    return num

def arithmetic_encoding(s):
    
    length = len(s)
    one=0
    zero=0
    
    for i in range(length):
        if(s[i]=='0'):
            zero=zero+1;
        else:
            one=one+1;
    p=[zero/length, one/length]
    
    Fx = [p[0],p[0]+p[1]]
    Tx = [p[0]/2, p[0]+p[1]/2]
    
    number_of_digit = [1+ math.ceil(math.log2(1.0/p[0])), 1+ math.ceil(math.log2(1.0/p[1])) ]
    #print(number_of_digit)
    
    bin_of_Tx = [to_bin(Tx[0], number_of_digit[0]), to_bin(Tx[1], number_of_digit[1])]
    
    bin_of_Tx = [bin_of_Tx[0][1:],bin_of_Tx[1][1:] ]
    
    #print(Tx)
    #print(bin_of_Tx)
    
    print("Code for '0' is : " + bin_of_Tx[0])
    print("Code for '1' is : " + bin_of_Tx[1])
    
    encoded_string = ""
    for i in range(length) :
        if (s[i]=='0'):
            encoded_string = encoded_string + bin_of_Tx[0];
        else:
            encoded_string = encoded_string +bin_of_Tx[1];
  
    print("Encoded String is : " + encoded_string)
    
    return bin_of_Tx , encoded_string;


def arithmetic_decoding(code,s):
    # s in encoded string
    # code is the dictionary map of character and there codes
    decoded_string = ""
    current=""
    for i in range(len(s)):
        current = current + s[i]
        if(current==code[0]):
            decoded_string = decoded_string + '0'
            current=""
        elif (current==code[1]):
            decoded_string = decoded_string+ '1'
            current=""
    
    print("Decoded string is : " + decoded_string)








def arithmetic_encoding_2(s):
    
    length = len(s)
    one=0
    zero=0
    
    for i in range(length):
        if(s[i]=='0'):
            zero=zero+1;
        else:
            one=one+1;
    p=[zero/length, one/length]
    
    cpr = [p[0],p[0]+p[1]]
    newcpr = [0,p[0],p[0]+p[1]]
    
    #print(cpr)
    #print(newcpr)
    
    print(cpr)
    
    low =0
    high =1
    
    for i in range(length):
        if (s[i]=='0'):
            Range = high-low
            high = low + Range*cpr[0]
            low = low + Range*newcpr[0]
        else:
            Range = high-low
            high = low + Range*cpr[1]
            low = low + Range*newcpr[1]
                
    tag = (low+high)/2
    
    print(tag)
    

	
def arithmetic_decoding2(s,tag) :
    
    # s is the string to be decoded 
    # tag is the unique value for decoding
    
    length = len(s)
    
    one=0
    zero=0
    
    for i in range(length):
        if(s[i]=='0'):
            zero=zero+1;
        else:
            one=one+1;
    p=[zero/length, one/length]
    
    cpr = [p[0],p[0]+p[1]]
    newcpr = [0,p[0],p[0]+p[1]]
    
    #print(cpr)
    #print(newcpr)
    
    
    decoded_str=""
    for i in range(length):
        #print(tag)
        for j in range(2) :
            if((tag > newcpr[j]) & (tag < cpr[j])) :
                decoded_str = decoded_str + str(j) 
                tag = (tag - newcpr[j])/p[j]
                break
    
    print("Decode String is :")
    print(decoded_str)
    



num_chunks = 7
k = int(len(bin_inp)/num_chunks)


def arithmetic() :
    for i in range(num_chunks) :
        print("Chunk : " + str(1+i))
        chunk = bin_inp[i*k:(i+1)*k]
        x,y=arithmetic_encoding(chunk)
        arithmetic_decoding(x,y)
        
	
arithmetic()


