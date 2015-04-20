
entries = 6
friends = 3

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

for i in range(friends):
    for j in range(friends,entries):
        if Matrix[i][j] < 0 and i > 0:
            Matrix[0][i] -= Matrix[i][j]
            Matrix[0][j] += Matrix[i][j]
            Matrix[i][j] = 0
        if Matrix[i][j] > 0 and j > friends:
            Matrix[i][friends] += Matrix[i][j]
            Matrix[friends][j] += Matrix[i][j]
            Matrix[i][j] = 0
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
