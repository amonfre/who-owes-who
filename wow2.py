
entries = 6
friends = 3

friendList = [1,1,1,2,2,2]

Matrix = [[0 for x in range(entries)] for y in range(entries)]
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

counter1 = 0
newfriends = [0]

while (len(friendList)) > 0:
    firstFriend = friendList[0]
    while len(friendList) > 0 and friendList[0] == firstFriend:
        friendList.pop(0)
        counter1 += 1
    newfriends.append(counter1)
 
print newfriends

while newfriends[1] != len(Matrix):
    for i in range(newfriends[0],newfriends[1]):
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

print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))
       
for i in range(entries):
    for j in range(i):
        Matrix[i][j] = -Matrix[j][i]
   
networth = [0 for x in range(entries)]  
for i in range(entries):
    for j in range(entries):
        networth[i] += Matrix[i][j]

Transactions = -1
for i in range(entries):
    if networth[i] != 0:
        Transactions += 1
print networth
print Transactions

