import copy
entries = int(raw_input())

Matrix = [[0 for x in range(entries)] for y in range(entries)]
friends = []

#Create orginal payment Matrix
#Create the original friend Matrix
cur_per = 0
for i in range(entries):
	friend = map(int, raw_input().split())
	friend.append(i)
	#print friend
	for j in range(len(friend)):
	    if friend[j] == cur_per:
	        friend.pop(j)
	    elif friend[j] == -1:
	        friend = []
	        break
	cur_per += 1
	friends.append(friend)
	edges = raw_input().split(" ")
	for edge in edges:
		edge_value = map(int, edge.split(","))
		if edge_value[0] != -1:
			Matrix[i][edge_value[0]] = edge_value[1]
'''print "Original Matrix"
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))
#print('\n')
print friends'''

count = 0
Worth_Matrix = [[0 for x in range(entries)] for y in range(entries)]
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if  Matrix[i][j] != 0:
            count += 1
            Worth_Matrix[i][j] += Matrix[i][j]
            Worth_Matrix[j][i] += -Matrix[i][j]
            '''print 'Worth Matrix'    
            print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
                for row in Worth_Matrix]))'''
#Calculate the networth of each individual
#print 'Transactions'
#print count

networth = [0 for x in range(entries)]  
for i in range(entries):
    for j in range(entries):
        networth[i] += Worth_Matrix[i][j]
print networth    
    
#Try every possible combonation and find the optimal
tracker = 0
transactions = 0
check = 0
first = 0
second = 1
while check == 0:
    if all(vals == 0 for vals in networth):
        check = 1
    for i in range(len(networth) - first):
        for j in range(len(networth) - second):
            if networth[first] != 0 and networth[second] != 0:
                networth[second] += networth[first]
                networth[first] = 0
                transactions += 1
                first += second
                second += 1
            elif networth[first] == 0:
                first += 1
                second += 1
            elif networth[second] == 0:
                second += 1
print networth    
print transactions    
            
