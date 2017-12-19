# id is associated with objects, and python is pass by objects

x = 3
y = 4
print x, id(x) #id1
print y, id(y) #id2

def swap (x, y): 
	print x, id(x) #id1
	print y, id(y) #id2
	tmp = x 
	x = y
	y = tmp
	print x, id(x) #id2
	print y, id(y) #id1
	return x, y

print "in swap---- "
swap(x, y)

print "out swap---"
print x, id(x) #id1
print y, id(y) #id2


x, y = y, x
# is this equivalent to x = y; y = x
# no
# x, y = [y, x]
