
'''Matrix = [[0 for x in range(entries)] for y in range(entries)]
Matrix [0][1] = -10
Matrix [0][3] = -10
Matrix [1][2] = -10
Matrix [1][3] = -10
Matrix [1][4] = 10
Matrix [2][3] = 10
Matrix [2][5] = -10
Matrix [3][4] = 10
Matrix [4][5] = -10

print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))
print ('\n')'''
import copy
entries = int(raw_input())

Matrix = [[0 for x in range(entries)] for y in range(entries)]
friends = []

#Create orginal payment Matrix
for i in range(entries):
	friend = map(int, raw_input().split())
	friend.append(i)
	check_friends = False
	for j in range(len(friends)):
		if friend[0] in friends[j]:
			check_friends = True
		elif friend[0] == -1:
			check_friends = True
	if check_friends == False:
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

#Create list for friend grou connections
friendList = [0 for x in range(entries)]
count1 = 0
count2 = 1
for i in range(len(friends)):
    for j in range(len(friends[i])):
         friendList[count1] = count2
         count1 += 1
    count2 += 1

counter1 = 0
newfriends = [0]

#Create a list of number of friends in each group
while (len(friendList)) > 0:
    firstFriend = friendList[0]
    while len(friendList) > 0 and friendList[0] == firstFriend:
        friendList.pop(0)
        counter1 += 1
    newfriends.append(counter1)
newfriends_copy = copy.deepcopy(newfriends)
newfriends_copy2 = copy.deepcopy(newfriends)
print newfriends
#Re-calculate the matrix to fit structure used in below algorithm
for i in range(entries):
    for j in range(i):
        if Matrix[i][j] > 0:
            Matrix[j][i] = -Matrix[i][j]
            Matrix[i][j] = 0
            
'''print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))         
print('\n')'''

#Re-calculate the matrix to minimize payments between friend groups
while newfriends[1] != len(Matrix):
    for i in range(newfriends[1]):
        for j in range(newfriends[1],entries):
            if Matrix[i][j] < 0 and i > 0:
                Matrix[newfriends[0]][i] -= Matrix[i][j]
                Matrix[newfriends[0]][j] += Matrix[i][j]
                Matrix[i][j] = 0
            if Matrix[i][j] > 0 and j > newfriends[1] and j < newfriends[2]:
                Matrix[i][newfriends[1]] += Matrix[i][j]
                Matrix[newfriends[1]][j] += Matrix[i][j]
                Matrix[i][j] = 0
    newfriends.pop(0)

'''print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))'''
       
for i in range(entries):
    for j in range(i):
        Matrix[i][j] = -Matrix[j][i]

#Calculate the networth of each individual
networth = [0 for x in range(entries)]  
for i in range(entries):
    for j in range(entries):
        networth[i] += Matrix[i][j]

#Determine the total number of transactions
Transactions = -1
for i in range(entries):
    if networth[i] != 0:
        Transactions += 1
        
finalMatrix = [[0 for x in range(entries)] for y in range(entries)]

new_networth = []

#Create networth Matrix
while newfriends_copy[0] != len(networth):
    hold_list = []
    for i in range(newfriends_copy[0], newfriends_copy[1]):
        hold_list.append(networth[i])
    new_networth.append(hold_list)
    newfriends_copy.pop(0)
listCounter = 0 
indexCounter = 0
print new_networth

#Resolve the optimal payment method within each friend group
while listCounter < len(new_networth):
    listLen = len(new_networth[listCounter])
    while listLen > 1:
        if all(x==0 for x in new_networth[listCounter]):
            listCounter += 1
        maxVal = max(value for value in new_networth[listCounter] if value is not 0)
        maxIndex = new_networth[listCounter].index(maxVal)
        minVal = min(value for value in new_networth[listCounter] if value is not 0)
        minIndex = new_networth[listCounter].index(minVal)
        if maxIndex != minIndex:
            new_networth[listCounter][maxIndex] += new_networth[listCounter][minIndex]
            finalMatrix[indexCounter+minIndex][indexCounter+maxIndex] += new_networth[listCounter][minIndex]
            new_networth[listCounter][minIndex] = 0
        listLen -= 1 
    indexCounter += len(new_networth[listCounter])
    listCounter += 1
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in finalMatrix]))
print('\n')
listCounter = 0
listCounter2 = 1
indexCounter = 0

#Resolve the optimal payment method between friend groups and compute 
#the optimal Matrix to represnt the solution
while listCounter2 < (len(new_networth)):
    if all(x==0 for x in new_networth[listCounter]):
        listCounter += 1
        listCounter2 += 1
    elif all(x==0 for x in new_networth[listCounter2]):
        listCounter2 += 1
    firstVal = min(value for value in new_networth[listCounter] if value is not 0)
    firstIndex = new_networth[listCounter].index(firstVal)
    secVal = min(value for value in new_networth[listCounter2] if value is not 0)
    secIndex = new_networth[listCounter2].index(secVal)
    if secVal > firstVal:
        new_networth[listCounter2][secIndex] += new_networth[listCounter][firstIndex]
        finalMatrix[newfriends_copy2[listCounter2]+secIndex][newfriends_copy2[listCounter]+firstIndex] += secVal
        new_networth[listCounter][firstIndex] = 0
        listCounter = listCounter2 - 1
    else:
        new_networth[listCounter][firstIndex] += new_networth[listCounter2][secIndex]
        finalMatrix[newfriends_copy2[listCounter2]+secIndex][newfriends_copy2[listCounter]+firstIndex] += secVal
        new_networth[listCounter2][secIndex] = 0
        listCounter -= 1
    listCounter += 1
    listCounter2 += 1
    indexCounter += 1
#Display the optimal Matrix
print "Optimal Matrix"
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in finalMatrix]))
