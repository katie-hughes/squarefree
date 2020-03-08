import numpy as np

res = 0
sf = 0

nums = range(1, 152)

for x in range(1, 151):
	if(x%4 == 0):
		print x, "is divisible by 4"
		nums[x] = 4
		res += 1
		pass
	elif(x%9 ==0):
		print x, "is divisible by 9"
		res +=1
		nums[x] = 9
		pass
	elif(x%16 == 0):
		print x, "is divisible by 16"
		res +=1
		nums[x] = 16
		pass
	elif(x%25 == 0):
		print x, "is divisible by 25"
		res +=1
		nums[x] = 25
		pass
	elif(x%36 == 0):
		print x, "is divisible by 36"
		res +=1
		nums[x] = 36
		pass
	elif(x%49 == 0):
		print x, "is divisible by 49"
		res += 1
		nums[x] = 49
		pass
	elif(x%64 == 0):
		print x, "is divisible by 64"
		res += 1
		nums[x] = 64
		pass
	elif (x%81 == 0):
		print x, "is divisible by 81"
		res +=1
		nums[x] = 81
		pass
	elif(x%100 == 0):
		print x, "is divisible by 100"
		nums[x] = 100
		res += 1
		pass
	elif (x%121 == 0):
		print x, "is divisible by 121"
		res +=1
		nums[x] = 121
		pass
	elif (x%144 == 0):
		print x, "is divisible by 144"
		res +=1
		nums[x] = 144
		pass
	else:
		print x, "is SQUAREFREE!!"
		sf += 1
		nums[x] = 0

#print "res is", res

print "number squarefree is", sf
