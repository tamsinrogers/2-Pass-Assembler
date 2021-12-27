# Template by Bruce A. Maxwell, 2015
#
# implements a simple assembler for the following assembly language
# 
# - One instruction or label per line.
#
# - Blank lines are ignored.
#
# - Comments start with a # as the first character and all subsequent
# - characters on the line are ignored.
#
# - Spaces delimit instruction elements.
#
# - A label ends with a colon and must be a single symbol on its own line.
#
# - A label can be any single continuous sequence of printable
# - characters; a colon or space terminates the symbol.
#
# - All immediate and address values are given in decimal.
#
# - Address values must be positive
#
# - Negative immediate values must have a preceeding '-' with no space
# - between it and the number.
#

# Language definition:
#
# LOAD D A	 - load from address A to destination D
# LOADA D A	 - load using the address register from address A + RE to destination D
# STORE S A	 - store value in S to address A
# STOREA S A - store using the address register the value in S to address A + RE
# BRA L		 - branch to label A
# BRAZ L	 - branch to label A if the CR zero flag is set
# BRAN L	 - branch to label L if the CR negative flag is set
# BRAO L	 - branch to label L if the CR overflow flag is set
# BRAC L	 - branch to label L if the CR carry flag is set
# CALL L	 - call the routine at label L
# RETURN	 - return from a routine
# HALT		 - execute the halt/exit instruction
# PUSH S	 - push source value S to the stack
# POP D		 - pop form the stack and put in destination D
# OPORT S	 - output to the global port from source S
# IPORT D	 - input from the global port to destination D
# ADD A B C	 - execute C <= A + B
# SUB A B C	 - execute C <= A - B
# AND A B C	 - execute C <= A and B	 bitwise
# OR  A B C	 - execute C <= A or B	 bitwise
# XOR A B C	 - execute C <= A xor B	 bitwise
# SHIFTL A C - execute C <= A shift left by 1
# SHIFTR A C - execute C <= A shift right by 1
# ROTL A C	 - execute C <= A rotate left by 1
# ROTR A C	 - execute C <= A rotate right by 1
# MOVE A C	 - execute C <= A where A is a source register
# MOVEI V C	 - execute C <= value V
#

# 2-pass assembler
# pass 1: read through the instructions and put numbers on each instruction location
#		  calculate the label values
#
# pass 2: read through the instructions and build the machine instructions
#

import sys

# converts d to an 8-bit 2-s complement binary value
def dec2comp8( d, linenum ):
	try:
		if d > 0:
			l = d.bit_length()
			v = "00000000"
			v = v[0:8-l] + format( d, 'b')
		elif d < 0:
			dt = 128 + d
			l = dt.bit_length()
			v = "10000000"
			v = v[0:8-l] + format( dt, 'b')[:]
		else:
			v = "00000000"
	except:
		print('Invalid decimal number on line %d' % (linenum))
		exit()

	return v

# converts d to an 8-bit unsigned binary value
def dec2bin8( d, linenum ):
	if d > 0:
		l = d.bit_length()
		v = "00000000"
		v = v[0:8-l] + format( d, 'b' )
	elif d == 0:
		v = "00000000"
	else:
		print('Invalid address on line %d: value is negative' % (linenum))
		exit()

	return v


# Tokenizes the input data, discarding white space and comments
# returns the tokens as a list of lists, one list for each line.
#
# The tokenizer also converts each character to lower case.
def tokenize( fp ):
	tokens = []

	# start of the file
	fp.seek(0)

	lines = fp.readlines()

	# strip white space and comments from each line
	for line in lines:
		ls = line.strip()
		uls = ''
		for c in ls:
			if c != '#':
				uls = uls + c
			else:
				break

		# skip blank lines
		if len(uls) == 0:
			continue

		# split on white space
		words = uls.split()

		newwords = []
		for word in words:
			newwords.append( word.lower() )

		tokens.append( newwords )

	return tokens


# reads through the file and returns a dictionary of all location
# labels with their line numbers
def pass1( tokens ):
	#dictionary = dict([])			# set up an empty dictionary
	#instructions = []					# set up an empty list for the instructions
	
	#i = 0		
	
	# dictionary = { symbol : line number of the symbol, symbol : line number of the symbol }					
	
	#while i < len(tokens):				# read through the file
	#	line = tokens[i]				# each line of the file
	#	if line[-1].endswith(':'):		# if the last token in the line is a :, this indicates that it is a symbol
	#		dictionary[ line[0]	 ] = i; # add the symbol to the dictionary
	#		break
	#	else: 
	#		instructions.append(line)	# add the instruction to the list
	#		i = i+1							# go to the next line
	
	# remove the lines with labels from the tokens 
	#for i in tokens:					# for each line in the tokens list
		#if i[-1].endswith(':'):			# if the last character in the line is a :, this indicates that it is a symbol
		#	tokens.remove(i)			   # remove the line from the tokens list
	
	num = 0
	dict = {}
	instructions = []
	
	for i in tokens:
		if i[0].endswith(":"):
			dict[i[0]] = num
		else:
			num += 1
			instructions.append(i)
	
	return dict


def pass2( tokens, labels ):

	print(labels)

	binaryinstructions = []				# list to hold the instructions
	
	for instruction in tokens:
		code = " "

		if instruction[0] == "load":
		
			if len(instruction) < 3:
				print("LOAD error: provide a destination & an address")
		
			code += "00000"
			
			# destination (from table B)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			
			# address
			code += instruction[2]
			
			
		elif instruction[0] == "loada" :
		
			if len(instruction) < 3:
				print("LOADA error: provide a destination & an address")
		
			code += "00001"
			
			# destination (from table B)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			
			# address
			code += instruction[2]
		
		elif instruction[0] == "store" :
			
			if len(instruction) < 3:
				print("STORE error: provide a source & an address")
		
			code += "00010"
			
			# source (from table B)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			
			# address
			code += instruction[2]
		
		elif instruction[0] == "storea" :
			
			if len(instruction) < 3:
				print("STOREA error: provide a source & an address")
		
			code += "00011"
			
			# source (from table B)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			
			# address
			code += instruction[2]
		
		elif instruction[0] == "bra" :
			
			if len(instruction) < 2:
				print("BRANCH error: provide a label to branch to")
		
			code += "0010"
			code += "0000"
			
			# address
			code += instruction[1]
		
		elif instruction[0] == "braz" :
		
			if len(instruction) < 2:
				print("BRANCH error: provide a label to branch to")
			
			code += "00110000"
			key = instruction[1]
			
			print(key)
			print(labels.get(key))
			
			x = dec2bin8(int(labels.get(key)), int(labels.get(key)))
			code += str(x)
		
		elif instruction[0] == "bran" :
		
			if len(instruction) < 2:
				print("BRANCH error: provide a label to branch to")
		
			code += "00110001"
			key = instruction[1]
			x = dec2bin8(int(labels[key]), int(labels[key]))
			code += str(x)
		
		elif instruction[0] == "brao" :
			
			if len(instruction) < 2:
				print("BRANCH error: provide a label to branch to")
		
			code += "00110010"
			key = instruction[1]
			x = dec2bin8(int(labels[key]), int(labels[key]))
			code += str(x)
		
		elif instruction[0] == "brac" :
		
			if len(instruction) < 2:
				print("BRANCH error: provide a label to branch to")
		
			code += "00110011"
			key = instruction[1]
			x = dec2bin8(int(labels[key]), int(labels[key]))
			code += str(x)
		
		elif instruction[0] == "call" :
		
			if len(instruction) < 2:
				print("CALL error: provide a label to call")
		
			code += "00110100"
			
			key = instructions[1]
			x = dec2bin8(int(labels[key]), int(labels[key]))
			code += str(x)
			
			# address
			# code += instruction[1]
		
		elif instruction[0] == "return" :
			code += "0011100000000000"
		
		elif instruction[0] == "halt" :
			code += "0011110000000000"
		
		elif instruction[0] == "push" :
		
			if len(instruction) < 2:
				print("PUSH error: provide a source to push onto the stack")
		
			code += "0100"
			
			# source (from table c)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "pc":
				code += "110"
			elif instruction[1] == "cr":
				code += "111"
			
			code += "000000000"
		
		elif instruction[0] == "pop" :
		
			if len(instruction) < 2:
				print("POP error: provide a source to pop from the stack")
		
			code += "0101"
			
			# source (from table c)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "pc":
				code += "110"
			elif instruction[1] == "cr":
				code += "111"
			
			code += "000000000"
		
		elif instruction[0] == "oport" :
		
			if len(instruction) < 2:
				print("OPORT error: provide a source to send to the output port")
		
			code += "0110"
			
			# source (from table D)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "pc":
				code += "110"
			elif instruction[1] == "ir":
				code += "111"
			
			code += "000000000"
		
		elif instruction[0] == "iport" :
		
			if len(instruction) < 2:
				print("OPORT error: provide a destination to receive the value of the input port")
		
			code += "0111"
			
			# destination (from table B)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			
			code += "000000000"
		
		elif instruction[0] == "add" :
		
			if len(instruction) < 4:
				print("ADD error: provide two sources and a destination")
		
			code += "1000"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			# source B (from table E)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
			elif instruction[2] == "0000000000000000":
				code += "110"
			elif instruction[2] == "1111111111111111":
				code += "111"
			
			code += "000"
			
			# destination (from table B)
			if instruction[3] == "ra":
				code += "000"
			elif instruction[3] == "rb":
				code += "001"
			elif instruction[3] == "rc":
				code += "010"
			elif instruction[3] == "rd":
				code += "011"
			elif instruction[3] == "re":
				code += "100"
			elif instruction[3] == "sp":
				code += "101"
			
		elif instruction[0] == "sub" :
		
			if len(instruction) < 4:
				print("SUB error: provide two sources and a destination")
		
			code += "1001"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			# source B (from table E)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
			elif instruction[2] == "0000000000000000":
				code += "110"
			elif instruction[2] == "1111111111111111":
				code += "111"
			
			code += "000"
			
			# destination (from table B)
			if instruction[3] == "ra":
				code += "000"
			elif instruction[3] == "rb":
				code += "001"
			elif instruction[3] == "rc":
				code += "010"
			elif instruction[3] == "rd":
				code += "011"
			elif instruction[3] == "re":
				code += "100"
			elif instruction[3] == "sp":
				code += "101"
		
		elif instruction[0] == "and" :
		
			if len(instruction) < 4:
				print("AND error: provide two sources and a destination")
		
			code += "1010"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			# source B (from table E)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
			elif instruction[2] == "0000000000000000":
				code += "110"
			elif instruction[2] == "1111111111111111":
				code += "111"
			
			code += "000"
			
			# destination (from table B)
			if instruction[3] == "ra":
				code += "000"
			elif instruction[3] == "rb":
				code += "001"
			elif instruction[3] == "rc":
				code += "010"
			elif instruction[3] == "rd":
				code += "011"
			elif instruction[3] == "re":
				code += "100"
			elif instruction[3] == "sp":
				code += "101"
			
		elif instruction[0] == "or" :
		
			if len(instruction) < 4:
				print("OR error: provide two sources and a destination")
		
			code += "1011"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			# source B (from table E)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
			elif instruction[2] == "0000000000000000":
				code += "110"
			elif instruction[2] == "1111111111111111":
				code += "111"
			
			code += "000"
			
			# destination (from table B)
			if instruction[3] == "ra":
				code += "000"
			elif instruction[3] == "rb":
				code += "001"
			elif instruction[3] == "rc":
				code += "010"
			elif instruction[3] == "rd":
				code += "011"
			elif instruction[3] == "re":
				code += "100"
			elif instruction[3] == "sp":
				code += "101"
		
		elif instruction[0] == "xor" :
		
			if len(instruction) < 4:
				print("XOR error: provide two sources and a destination")
		
			code += "1100"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			# source B (from table E)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
			elif instruction[2] == "0000000000000000":
				code += "110"
			elif instruction[2] == "1111111111111111":
				code += "111"
			
			code += "000"
			
			# destination (from table B)
			if instruction[3] == "ra":
				code += "000"
			elif instruction[3] == "rb":
				code += "001"
			elif instruction[3] == "rc":
				code += "010"
			elif instruction[3] == "rd":
				code += "011"
			elif instruction[3] == "re":
				code += "100"
			elif instruction[3] == "sp":
				code += "101"
		
		elif instruction[0] == "shiftl" :
		
			if len(instruction) < 3:
				print("SHIFTL error: provide a source and a destination")
		
			code += "11010"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			code += "00000"
			
			# destination (from table B)
			if instruction[2] == "ra":
				code += "000"
			elif instruction [2] == "rb":
				code += "001"
			elif instruction [2] == "rc":
				code += "010"
			elif instruction [2] == "rd":
				code += "011"
			elif instruction [2] == "re":
				code += "100"
			elif instruction [2] == "sp":
				code += "101"
		
		elif instruction[0] == "shiftr" :
		
			if len(instruction) < 3:
				print("SHIFTR error: provide a source and a destination")
		
			code += "11011"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			code += "00000"
			
			# destination (from table B)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
		
		elif instruction[0] == "rotl" :
		
			if len(instruction) < 3:
				print("ROTL error: provide a source and a destination")
		
			code += "11100"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			code += "00000"
			
			# destination (from table B)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
		
		elif instruction[0] == "rotr" :
		
			if len(instruction) < 3:
				print("ROTR error: provide a source and a destination")
		
			code += "11101"
			
			# source A (from table E)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "0000000000000000":
				code += "110"
			elif instruction[1] == "1111111111111111":
				code += "111"
			
			code += "00000"
			
			# destination (from table B)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
		
		elif instruction[0] == "move" :
		
			if len(instruction) < 3:
				print("MOVE error: provide a source and a destination")
		
			code += "1111"
			
			# source (from table D)
			if instruction[1] == "ra":
				code += "000"
			elif instruction[1] == "rb":
				code += "001"
			elif instruction[1] == "rc":
				code += "010"
			elif instruction[1] == "rd":
				code += "011"
			elif instruction[1] == "re":
				code += "100"
			elif instruction[1] == "sp":
				code += "101"
			elif instruction[1] == "pc":
				code += "110"
			elif instruction[1] == "ir":
				code += "111"
		
			code += "00000"
			
			# destination (from table B)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
			
		elif instruction[0] == "movei" :
		
			if len(instruction) < 3:
				print("MOVEI error: provide a source and a destination")
			
			code += "11111"
			
			code += dec2comp8(int(instruction[1]), '1')
			
			# destination (from table B)
			if instruction[2] == "ra":
				code += "000"
			elif instruction[2] == "rb":
				code += "001"
			elif instruction[2] == "rc":
				code += "010"
			elif instruction[2] == "rd":
				code += "011"
			elif instruction[2] == "re":
				code += "100"
			elif instruction[2] == "sp":
				code += "101"
				
		binaryinstructions.append(code)		# add the instruction to the list
	
	return binaryinstructions				# return the list of instructions

def main( argv ):
	if len(argv) < 2:
		print('Usage: python %s <filename>' % (argv[0]))
		exit()

	fp = open( argv[1], 'rU' )				# read the text file
	
	tokens = tokenize( fp )
	dict = pass1(tokens)
	instructions = pass2(tokens, dict)
	
	fp = open( argv[2], 'w')				# write to the .mif file
	
	fp.write("-- program memory file for " + argv[2]
	+ "\n" + "DEPTH = 256;" + "\n" + "WIDTH = 16;" + "\n" + "ADDRESS_RADIX = HEX;"
	+ "\n" + "DATA_RADIX = BIN;" + "\n" + "CONTENT" + "\n" + "BEGIN" + "\n")
	
	print("-- program memory file for " + argv[2]
	+ "\n" + "DEPTH = 256;" + "\n" + "WIDTH = 16;" + "\n" + "ADDRESS_RADIX = HEX;"
	+ "\n" + "DATA_RADIX = BIN;" + "\n" + "CONTENT" + "\n" + "BEGIN" + "\n")
	
	line = -01
	
	for i in instructions:					# write each line of the instructions
		line += 1
		if line == len(instructions)-1:
			begin = "0" + str(line)
			if line > 9:
				begin = hex(line)
			print("[" + begin + "..FF] : 1111111111111111;")
			fp.write("[" + begin + "..FF] : 1111111111111111;")
			print("\n")
			break
		print("%02X : %s;" % (line, i))
		fp.write("%02X : %s;" % (line, i))
		fp.write(i)
		fp.write("\n")	 

	fp.close()

	return

if __name__ == "__main__":
	main(sys.argv)


	