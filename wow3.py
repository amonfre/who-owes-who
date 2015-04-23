import copy

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
Matrix = [[0 for x in range(num)] for y in range(num)]
#empty list of friend groups
friends = []

#build list of friend groups
cur_per = 0
for i in range(num):
	friend = people[i].friends
	friend.append(i)
	for j in range(len(friend)):
	    if friend[j] == cur_per:
	        friend.pop(j)
	    elif friend[j] == -1:
	        friend = []
	        break
	cur_per += 1
	friends.append(friend)
	'''check_friends = False
	if len(friend) == 1:
		check_friends = True
	elif friend in friends:
		check_friends = True	
	if check_friends == False:
		friends.append(friend)'''
	#build graph of transactions
	edges = people[i].payments
	for edge in edges:
		Matrix[i][edge[0]] = edge[1]

#print "original graph:"
#print Matrix

#initialize new graph for optimization
#new_graph = copy.deepcopy(graph)
'''
import copy
entries = int(raw_input())
num = entries

Matrix = [[0 for x in range(num)] for y in range(num)]
friends = []

#Create orginal payment Matrix
#Create the original friend Matrix
cur_per = 0
for i in range(num):
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
#print "Original Matrix"
#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      #for row in Matrix]))
'''
count = 0
Worth_Matrix = [[0 for x in range(num)] for y in range(num)]
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if  Matrix[i][j] != 0:
            count += 1
            Worth_Matrix[i][j] += Matrix[i][j]
            Worth_Matrix[j][i] += -Matrix[i][j]
#Calculate the networth of each individual
#print 'Transactions'
#print count

networth = [0 for x in range(num)]  
for i in range(num):
    for j in range(num):
        networth[i] += Worth_Matrix[i][j]
#print networth       
    
#Refine the matrix to find one of the optimal solutions (There could be multiple)
#We do this before we account for friend groups to attempt to decrease the total 
#amount of payments

Matrix = [[0 for x in range(num)] for y in range(num)]
listCounter1 = 0
listCounter2 = 1
#Find any networths that sum to 0 in the list
while listCounter1 < len(networth):
    listCounter2 = 0
    while listCounter2 < len(networth):
        if networth[listCounter1] == -networth[listCounter2] and networth[listCounter1] != 0:
            if networth[listCounter1] > 0:
                Matrix[listCounter1][listCounter2] = networth[listCounter1]
            else:
                Matrix[listCounter2][listCounter1] = networth[listCounter2]
            networth[listCounter1] = 0
            networth[listCounter2] = 0
        listCounter2 += 1
    listCounter1 += 1
'''print 'New Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    for row in Matrix]))
print networth'''
#Resolve all other networths
breaker = 0
if all(x==0 for x in networth):
    breaker = 1
while breaker != 1:
    maxVal = max(value for value in networth if value is not 0)
    maxIndex = networth.index(maxVal)
    minVal = min(value for value in networth if value is not 0)
    minIndex = networth.index(minVal)
    if maxVal > -minVal:
        Matrix[maxIndex][minIndex] = -minVal 
        networth[maxIndex] += networth[minIndex]
        networth[minIndex] = 0
    else:
        Matrix[maxIndex][minIndex] = maxVal
        networth[minIndex] += networth[maxIndex]
        networth[maxIndex] = 0
    if all(x==0 for x in networth):
        breaker = 1

#Once we have compute an optimized solution, we want to have this solution be 
#compatible with our friend group constraints. That is, we have already
#minimized the total number of payments, but we now want to make sure that these
#payments are made within the closest trusted group, if this is possible.

#Refine the Matrix to redirect payments through a friend "channel"
#This function looks at payments of an individual outside of their friend group.
#It then finds, if it exists within four itterations, a friend "channel" to flow
#the payment through, so that we always have a friend to friend transaction.
#Four iterations was chosen simply because we felt this was the maximum 
#number of additional transactions tollerable for the tradeoff of better trusted
#transactions
New_Matrix = [[0 for x in range(num)] for y in range(num)]
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
             
#Find remaining payments outside of friend groups 
#This function aims to see if any two individuals within a friend group owes the
#same individual outside the group, and resolves the payment matrix accordingly 
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

#This function simply filters the matrix to take into account when two people 
#owe one another, simplifying two payments into one.
#Filter Matrix
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if New_Matrix[i][j] != 0 and New_Matrix[j][i] != 0:
            New_Matrix[i][j] -= New_Matrix[j][i]
            New_Matrix[j][i] = 0

#If we can initially find someone else in the friend group who owes someone else
#in the same non-conected friend groupwe want to combine these payments
count = 0
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        #if Matrix[i][j] != New_Matrix[i][j]:
        if New_Matrix[i][j] == 0 and Matrix[i][j] != New_Matrix[i][j]:           
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
#transactions and resolve them if possible
                    
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

#print 'New Matrix'    
#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      #for row in New_Matrix]))

#Finally, calculate the new networth of each individual and the total number of
#transactions necessary     
Worth_Matrix = [[0 for x in range(num)] for y in range(num)]
count = 0
for i in range(len(New_Matrix)):
    for j in range(len(New_Matrix)):
        if  New_Matrix[i][j] != 0:
            count += 1
            Worth_Matrix[i][j] += New_Matrix[i][j]
            Worth_Matrix[j][i] += -New_Matrix[i][j]

#Calculate the networth of each individual
networth = [0 for x in range(num)]  
for i in range(num):
    for j in range(num):
        networth[i] += Worth_Matrix[i][j]

Transactions = len(networth) - 1
#print 'Transactions'
#print count
