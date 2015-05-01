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
print "Original Matrix"
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))
#print('\n')
print friends

count = 0
Worth_Matrix = [[0 for x in range(num)] for y in range(num)]
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

networth = [0 for x in range(num)]  
for i in range(entries):
    for j in range(entries):
        networth[i] += Worth_Matrix[i][j]
print networth

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
            print 'l'
        listCounter2 += 1
    listCounter1 += 1
print 'New Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    for row in Matrix]))
print networth
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
