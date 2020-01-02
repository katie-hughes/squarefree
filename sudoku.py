import numpy as np


possibilities = []

def printboard(board):
	size = len(board)
	lines = np.sqrt(size)
	for x in range(0, size):
		if np.mod(x, lines) == 0: 
			print(" "), 
			for z in range(0, size): 
				print("__ "),
			print("\n"), 
		for y in range(0, size):
			num = board[x][y]
			if np.mod(y, lines) == 0: ###y == 0:
				print("|"),
			else:
				print(" "),
			if num == 0:
				print(" "), 
			else:
				print(num),
		print("\n"), 


def countarray(arr, number):
	count = 0
	size = len(arr)
	for x in range(0, size):
		if arr[x] == number:
			count += 1
	return count

def checkline(arr):
	size = len(arr)
	for x in range(1, size+1):
		count = countarray(arr, x);
		###print "there are", count, x, "'s in the array", arr
		if count > 1:
			return 0
	return 1
	

###check that there are no duplicates in rows/cols/boxes
def sanitycheck(board): 
	size = len(board)
	##print "Checking the rows..."
	for x in range(0, size):
		row = board[x]
		res = checkline(row)
		if res == 0:
			return 0 
	##print "Checking the columns..."
	transp = np.transpose(board)
	for y in range(0, size): 
		col = transp[y]
		res = checkline(col)
		if res == 0:
			return 0
	##print "Checking the boxes..."
	sqt = int(np.sqrt(size))
	for w in range(0, sqt):
		for x in range(0, sqt):
			box = np.zeros(size, dtype=int)
			count = 0; 
			for y in range(0, sqt):
				for z in range(0, sqt):
					num = board[sqt*w+y][sqt*x+z]
					##print "num is", num
					##print "position", str(sqt*w+y), str(sqt*x+z)
					box[count] = num
					count += 1
			count = 0
			res = checkline(box)
			if res == 0:
				return 0
	return 1

def fillinone(line):
	##first, check if there is only one number missing.
	c0 = countarray(line, 0)
	if c0 == 1:
		##find the missing number
		size = len(line)
		missing = 0
		for x in range(1, size+1):
			##counting occurences of x in the line.
			cx = countarray(line, x)
			if cx == 0:  ###x is the missing number. 
				missing = x
		print "the missing number in line", line, "is", missing
		for y in range(0, size):
			if line[y] == 0:
				line[y] = missing
		return 1
	else:
		return 0


def singlemissing(board):
	size = len(board)
	ret = 0
	print "Filling in one on the rows..."
	for x in range(0, size):
		row = board[x]
		res = fillinone(row)
		ret += res
	print "Filling in one on the columns..."
	transp = np.transpose(board)
	for y in range(0, size): 
		col = transp[y]
		res = fillinone(col)
		transp[y] = col
		board = np.transpose(transp)
		ret += res
	print "Filling in one on boxes..."
	sqt = int(np.sqrt(size))
	for w in range(0, sqt):
		for x in range(0, sqt):
			box = np.zeros(size, dtype=int)
			count = 0; 
			for y in range(0, sqt):
				for z in range(0, sqt):
					num = board[sqt*w+y][sqt*x+z]
					box[count] = num
					count += 1
			count = 0
			res = fillinone(box)
			### the issue: the array created for the box is separate from the board array. 
			for a in range(0, sqt):
				for b in range(0, sqt):
					board[sqt*w+a][sqt*x+b] = box[count]
					count += 1
			count = 0
			ret += res
	return ret 

##given an element, return the row/col/box arrays:
def selectrow(board, row, col):
	return board[row]

def selectcol(board, row, col):
	transp = np.transpose(board)
	return transp[col]

def selectbox(board, row, col):
	###this is the tricky one.
	size = len(board)
	sqt = int(np.sqrt(size))
	r = row / sqt
	c = col / sqt ###returns number in range (0, sqt)
	box = np.zeros(size, dtype=int)
	count = 0
	for x in range(0, sqt):
		for y in range(0, sqt):
			num = board[sqt*r+x][sqt*c+y]
			box[count] = num
			count += 1
	return box


##for a poss row/col/box
def poss_occurances(poss, number):
	size = len(poss)
	count = 0
	for x in range(0, size):
		current = poss[x]
		l = len(current)
		for y in range(0, l):
			if current[y] == number:
				count += 1
	return count

def poss_row(index):
	global possibilities
	return possibilities[index]

def poss_col(index):
	global possibilities
	size= len(possibilities)
	col_poss = []
	for x in range(0, size):
		col_poss.append(possibilities[x][index])
	return col_poss

def poss_box(index):
	global possibilities
	size = len(possibilities)
	sqt = int(np.sqrt(size))
	r = index / sqt
	c = index % sqt ###returns number in range (0, sqt)
	box_poss = []
	for x in range(0, sqt):
		for y in range(0, sqt):
			poss = possibilities[sqt*r+x][sqt*c+y]
			box_poss.append(poss)
	return box_poss

def box_index(size, row, col):
	sqt = int(np.sqrt(size))
	r = row / sqt
	c = col / sqt
	return sqt*r+c
	

def place(num, row, col, board):
	print "placing", num, "on board", row, col
	board[row][col] = num
	printboard(board)
	size = len(board)
	global possibilities
	##print "poss were", possibilities[row][col]
	possibilities[row][col] = []
	fill_possibilities(board)
	##remove_poss_row(row, num, board)
	##remove_poss_col(col, num, board)
	##remove_poss_box(box_index(size, row, col), num, board)
	oneoption(board)
	sc = sanitycheck(board)
	if sc==0:
		print "error"
		exit()

def remove_poss_row(index, num, board):
	print "removing", num, "from row", index
	global possibilities
	size = len(possibilities)
	for x in range(0, size):
		poss = possibilities[index][x]
		if num in poss:
			poss.remove(num)
			possibilities[index][x] = poss
		##if len(poss) == 1:
		##	n = poss[0]
		##	place(n, index, x, board)

def remove_poss_col(index, num, board):
	print "removing", num, "from column", index
	global possibilities
	size = len(possibilities)
	for x in range(0, size):
		poss = possibilities[x][index]
		if num in poss:
			poss.remove(num)
			possibilities[x][index] = poss
		##if len(poss) == 1:
		##	n = poss[0]
		##	place(n, x, index, board)

def remove_poss_box(index, num, board): 
	print "removing", num, "from box", index
	global possibilities
	size = len(possibilities)
	sqt = int(np.sqrt(size))
	r = index % sqt
	c = index / sqt
	for x in range(0, sqt):
		for y in range(0, sqt):
			poss = possibilities[sqt*r+x][sqt*c+y]
			if num in poss:
				poss.remove(num)
				possibilities[sqt*r+x][sqt*c+y] = poss
			##if len(poss) == 1:
			##	n = poss[0]
			##	place(n, sqt*r+x, sqt*c+y, board)


def fill_possibilities(board):
	size = len(board)
	changes = 0
	for x in range(0, size):
		for y in range(0, size):
			num = board[x][y]
			if num == 0:
				##print "Filling possibilities for board", x, y
				row = selectrow(board, x, y)
				col = selectcol(board, x, y)
				box = selectbox(board, x, y)
				global possibilities
				if len(possibilities[x][y]) == 0:
					options = range(1, size+1)
				else:
					options = possibilities[x][y]
				copy = list(options)
				###which numbers are allowed in box? 
				for z in copy: #range(1, size+1):
					cr = countarray(row, z)
					cc = countarray(col, z)
					cb = countarray(box, z)
					if ((cr == 1) or (cc == 1) or (cb == 1)):
						##z cannot go in position x, y. 
						##print "removing", z, "as an option from position", x, y
						options.remove(z)
						changes += 1
				##print "they are", options
				possibilities[x][y] = options
	return changes


def oneoption(board):
	print "one option"
	size = len(board)
	ret = 0
	global possibilities
	for x in range(0, size):
		for y in range(0, size):
			if len(possibilities[x][y]) == 1:
				num = possibilities[x][y][0]
				place(num, x, y, board)
				ret += 1
	return ret



def possibilities_manip1(board):
	ret = 0
	size = len(board)
	global possibilities
	print "manipulating rows"
	for x in range(0, size):
		row_poss = poss_row(x)
		print "row poss is", row_poss
		###count the occurences of each number in possibilities list. 
		for n in range(0, size):
			count = poss_occurances(row_poss, n)
			if count == 1:
				raw_input("count of something is one")
				##find the corresponding square. 
				##find the index in the possibilities list that has n. 
				for z in range(0, size):
					if n in row_poss[z]:
						##index z in row array.  
						place(n, x, z, board)
						ret += 1
	print "manipulating columns"
	for x in range(0, size):
		##doing the cols
		col_poss = poss_col(x)
		print "col poss is", col_poss
		for n in range(0, size):
			count = poss_occurances(col_poss, n)
			if count == 1:
				print "col is", x
				print "number is", n
				raw_input("count of something is one")
				for z in range(0, size):
					if n in col_poss[z]:
						##indez z in the col array
						place(n, z, x, board)
						ret += 1
	print "manipulating boxes"
	sqt = int(np.sqrt(size))
	for w in range(0, sqt):
		for x in range(0, sqt):
			box_poss = poss_box(sqt*w+x)
			print "box poss is", box_poss
			for n in range(0, size):
				count = poss_occurances(box_poss, n)
				if count == 1:
					print "number that only occurs once is", n
					raw_input("count of something is one")
					##finding the index of the number.
					index = 0
					for a in range(0, size):
						if n in box_poss[a]:
							index = a
					print "the index of the numbr in the box is", index
					itr = 0
					for b in range(0, sqt):
						for c in range(0, sqt):
							if itr == index:
								place(n, sqt*w+b, sqt*x+c, board)
								ret += 1
							itr += 1 
								
	return ret

def checkdone(board):
	##there just needs to be no zeros.
	size = len(board)
	for x in range(0, size):
		line = board[x]
		for y in range(0, size):
			num = line[y]
			if num == 0:
				return 0
	return 1


def main():
	print "Welcome to my sudoku solver!"
	size = input("Enter the size of the board:")
	print "Board size is", size
	if (int(np.sqrt(size)))**2 != size:
		print "size is not a square"
		exit()
	###creating the board
	board = np.zeros((size, size), dtype=int)
	printboard(board)

	##entering known values to board
	print "please enter in the known numbers separated by spaces (for empty, type 0)"
	for x in range(0, size):
		while(1):
			print "For row", x+1, ":", 
			s = raw_input("enter the numbers from left to right: ")
			numbers = map(int, s.split())
			print "numbers are", numbers
			if len(numbers) != size:
				print "bad!!"
			else:
				numbers = np.array(numbers)
				board[x] = numbers
				break
	print "This puzzle requires numbers from 1 -", size, "in each row, column, and square."
	printboard(board)
	raw_input("Press any key to continue.")
	print "Performing preliminary check"
	sc = sanitycheck(board)
	if sc == 0:
		print("There is an error with the numbers you inputted.")
		exit()
	print "All good! Onwards!"

	raw_input("Trying the filling in one method")
	ret = singlemissing(board)
	while(ret):
		print "ret is", ret
		ret = singlemissing(board)
		print "ret after is", ret

	done = checkdone(board)
	if done:
		print "It is solved!"
		printboard(board)
		exit()

	printboard(board)

	print "Initializing possibilities list"
	global possibilities
	for x in range(0, size):
		possibilities.append([])
		for y in range(0, size):
			possibilities[x].append([])

	raw_input("FIlling in possibilities")
	ret = fill_possibilities(board)
	printboard(board)
	

	raw_input("one option")
	ret = oneoption(board)
	while ret:
		ret = oneoption(board)

	done = checkdone(board)
	if done:
		print "It is solved!"
		printboard(board)
		exit()
	
	raw_input("Trying the possibilities manipulation")
	ret = possibilities_manip1(board)
	while(ret):
		ret = possibilities_manip1(board)
		printboard(board)

	done = checkdone(board)
	if done:
		print "It is solved!"
		printboard(board)
		exit()
	
	print "time to try something else."
	printboard(board)

if __name__ == "__main__":
	main()
