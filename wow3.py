'''import copy

#define class of people for input
class Person:
	def __init__(self, friends, payments):
		self.friends = friends
		self.payments = payments

#read in all people
people = input()

#find number of nodes
num = len(people)

#build empty transaction graph
graph = [[0 for x in range(num)] for y in range(num)]
#empty list of friend groups
friends = []

#build list of friend groups
for i in range(num):
	friend = set(people[i].friends)
	friend.add(i)
	check_friends = False
	if len(friend) == 1:
		check_friends = True
	elif friend in friends:
		check_friends = True	
	if check_friends == False:
		friends.append(friend)

	#build graph of transactions
	edges = people[i].payments
	for edge in edges:
		graph[i][edge[0]] = edge[1]

print "original graph:"
print graph

#initialize new graph for optimization
new_graph = copy.deepcopy(graph)
'''
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
print "Original Matrix"
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))
#print('\n')
print friends

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
print 'Transactions'
print count

networth = [0 for x in range(entries)]  
for i in range(entries):
    for j in range(entries):
        networth[i] += Worth_Matrix[i][j]
print networth       
        

#Refine the Matrix to redirect payments through a friend "channel"
New_Matrix = [[0 for x in range(entries)] for y in range(entries)]
x = 0
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if Matrix[i][j] != 0 and j not in friends[i]:
            found = 0
            #Search first neightbor nodes 
            for n in range(len(friends[i])):
                friend = friends[i][n]
                if j in friends[friend]:
                    New_Matrix[i][friend] += Matrix[i][j]
                    New_Matrix[friend][j] += Matrix[i][j]
                    Matrix[i][j] = 0
                    found = 1
                    '''print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
                        for row in New_Matrix]))'''
                    #print('\n')
            #Search second neighbor nodes
            if found != 1:
                for n in range(len(friends[i])):
                    friend2 = friends[i][n]
                    for k in range(len(friends[friend2])):
                        friend3 = friends[friend2][k]
                        if j in friends[friend3]:
                            New_Matrix[i][friend2] += Matrix[i][j]
                            New_Matrix[friend2][friend3] += Matrix[i][j]
                            New_Matrix[friend3][j] += Matrix[i][j]
                            Matrix[i][j] = 0
                            found = 1
            #Search third neighbor node
            if found != 1:
                for n in range(len(friends[i])):
                    friend2 = friends[i][n]
                    for k in range(len(friends[friend2])):
                        friend3 = friends[friend2][k]
                        for m in range(len(friends[friend3])):
                            friend4 = friends[friend3][m]
                            if j in friends[friend4]:
                                New_Matrix[i][friend2] += Matrix[i][j]
                                New_Matrix[friend2][friend3] += Matrix[i][j]
                                New_Matrix[friend3][friend4] += Matrix[i][j]
                                New_Matrix[friend4][j] += Matrix[i][j]
                                Matrix[i][j] = 0
            #Search fourth neighbor node
            if found != 1:
                for n in range(len(friends[i])):
                    friend2 = friends[i][n]
                    for k in range(len(friends[friend2])):
                        friend3 = friends[friend2][k]
                        for m in range(len(friends[friend3])):
                            friend4 = friends[friend3][m]
                            for g in range(len(friends[friend4])):
                                friend5 = friends[friend4][g]
                                if j in friends[friend4]:
                                    New_Matrix[i][friend2] += Matrix[i][j]
                                    New_Matrix[friend2][friend3] += Matrix[i][j]
                                    New_Matrix[friend3][friend4] += Matrix[i][j]
                                    New_Matrix[friend4][friend5] += Matrix[i][j]
                                    New_Matrix[friend5][j] += Matrix[i][j]
                                    Matrix[i][j] = 0
        else:
            New_Matrix[i][j] += Matrix[i][j]
            Matrix[i][j] = 0
                
'''print 'New friends only Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in New_Matrix]))
print('\n')'''
#Find remaining payments outside of friend groups  
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if New_Matrix[i][j] == 0 and Matrix[i][j] != New_Matrix[i][j]:           
            for n in range(len(friends[i])):
                #Does a friend owe the same person outside the group
                if Matrix[friends[i][n]][j] != 0:
                    New_Matrix[i][j] += Matrix[i][j] + Matrix[friends[i][n]][j]
                    New_Matrix[friends[i][n]][i] += Matrix[friends[i][n]][j]
                    Matrix[friends[i][n]][j] = 0
                    Matrix[i][j] = 0

'''print 'New Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in New_Matrix]))
print('\n')
print 'Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))
print('\n')'''

#Filter Matrix
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if New_Matrix[i][j] != 0 and New_Matrix[j][i] != 0:
            New_Matrix[i][j] -= New_Matrix[j][i]
            New_Matrix[j][i] = 0

'''print 'New Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in New_Matrix]))
print('\n')'''

count = 0
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        #if Matrix[i][j] != New_Matrix[i][j]:
        if New_Matrix[i][j] == 0 and Matrix[i][j] != New_Matrix[i][j]:           
            #New_Matrix[i][j] = -1
            for n in range(len(friends[i])):
                count = 0
                for m in range(len(Matrix)):
                #Does a friend owe someone in the same unconnected friend group 
                    if Matrix[friends[i][n]][m] < 0 and m in friends[j]:
                        New_Matrix[i][j] += Matrix[i][j] + Matrix[friends[i][n]][m]
                        New_Matrix[friends[i][n]][i] += Matrix[friends[i][n]][m]
                        Matrix[friends[i][n]][m] = 0
                        Matrix[i][j] = 0
                        count = 1
                    if Matrix[friends[i][n]][m] > 0 and m in friends[j]:
                        New_Matrix[i][j] += Matrix[i][j]
                        New_Matrix[j][m] += Matrix[friends[i][n]][m]
                        New_Matrix[friends[i][n]][j] += Matrix[friends[i][n]][m]
                        Matrix[friends[i][n]][m] = 0
                        Matrix[i][j] = 0
                        count = 1
            if count != 1:
                New_Matrix[i][j] += Matrix[i][j]
                Matrix[i][j] = 0
      
#Filter Matrix
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if New_Matrix[i][j] != 0 and New_Matrix[j][i] != 0:
            New_Matrix[i][j] -= New_Matrix[j][i]
            New_Matrix[j][i] = 0

#Due to the way we previously calculated the New_Matrix, some payments out of 
#friend groups that could be combined were skipped over. This is inevitable due 
#to the fact that we populate the New_Matrix from Matrix. While it may seem like 
#we could simply not do this, this is not true, because we must keep track of
#what values we have previously added in order to get the previous algorithm to 
#function properly
#Iterate over new Matrix to filter all aditional friend group-friend group 
#transactions
                    
for i in range(len(New_Matrix)):
    for j in range(len(New_Matrix)):
        if New_Matrix[i][j] != 0 and j not in friends[i]:
            for n in range(len(friends[j])): 
                if New_Matrix[i][friends[j][n]] != 0:
                    New_Matrix[i][j] += New_Matrix[i][friends[j][n]]
                    New_Matrix[j][friends[j][n]] += New_Matrix[i][friends[j][n]]
                    New_Matrix[i][friends[j][n]] = 0
            for k in range(len(friends[i])):
                for m in range(len(New_Matrix)):
                    if New_Matrix[friends[i][k]][m] != 0 and m in friends[j]:
                        New_Matrix[j][m] += New_Matrix[friends[i][k]][m] 
                        New_Matrix[i][j] += New_Matrix[friends[i][k]][m] 
                        New_Matrix[friends[i][k]][i] += New_Matrix[friends[i][k]][m]
                        New_Matrix[friends[i][k]][m] = 0
                if New_Matrix[friends[i][k]][j] != 0:
                    New_Matrix[i][j] += New_Matrix[friends[i][k]][j]
                    New_Matrix[friends[i][k]][i] += New_Matrix[friends[i][k]][j]
                    New_Matrix[friends[i][k]][j] = 0

print 'New Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in New_Matrix]))
      
Worth_Matrix = [[0 for x in range(entries)] for y in range(entries)]
count = 0
for i in range(len(New_Matrix)):
    for j in range(len(New_Matrix)):
        if  New_Matrix[i][j] != 0:
            count += 1
            Worth_Matrix[i][j] += New_Matrix[i][j]
            Worth_Matrix[j][i] += -New_Matrix[i][j]
            '''print 'Worth Matrix'    
            print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
                for row in Worth_Matrix]))'''
print 'Transactions'
print count
#Calculate the networth of each individual
networth = [0 for x in range(entries)]  
for i in range(entries):
    for j in range(entries):
        networth[i] += Worth_Matrix[i][j]

#Determine the minimum number of transactions
'''Transactions = 0
networth_copy = copy.deepcopy(networth)
c = 0
while c < len(networth_copy):
    if networth_copy[c] != 0:
        d = c + 1
        while d < len(networth_copy):
            if networth_copy[c] == -networth_copy[d]:
                networth_copy.pop(d)
                Transactions -= 1
            d += 1
        Transactions += 1
    c += 1'''
Transactions = len(networth) - 1
print networth
#print 'Max Transactions'
#print Transactions
print friends

#print 'Final Matrix'    
'''print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
                for row in Matrix]))'''
'''#Find friend groups whose networth is 0
for i in range(len(friends)):
    worth = networth[i]
    for j in range(len(friends[i])):
        worth += networth[friends[i][j]]
    if worth == 0:
        print i'''
    

