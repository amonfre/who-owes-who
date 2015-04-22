import copy
entries = int(raw_input())

Matrix = [[0 for x in range(entries)] for y in range(entries)]
friends = []

#Create orginal payment Matrix
cur_per = 0
for i in range(entries):
	friend = map(int, raw_input().split())
	friend.append(i)
	print friend
	for j in range(len(friend)):
	    if friend[j] == cur_per:
	        friend.pop(j)
	        print j
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
            #Search second neighbor nodes
            if found != 1:
                for n in range(len(friends[i])):
                    friend2 = friends[i][n]
                    for k in range(len(friends[friend2])):
                        friend3 = friends[friend2][k]
                        if j in friends[friend3]:
                            New_Matrix[i][friend3] += Matrix[i][j]
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
                                New_Matrix[i][friend4] += Matrix[i][j]
                                New_Matrix[friend2][friend3] += Matrix[i][j]
                                New_Matrix[friend3][friend4] += Matrix[i][j]
                                New_Matrix[friend4][j] += Matrix[i][j]
                                Matrix[i][j] = 0
            #Optional
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
                                    New_Matrix[i][friend5] += Matrix[i][j]
                                    New_Matrix[friend2][friend3] += Matrix[i][j]
                                    New_Matrix[friend3][friend4] += Matrix[i][j]
                                    New_Matrix[friend4][friend5] += Matrix[i][j]
                                    New_Matrix[friend5][j] += Matrix[i][j]
                                    Matrix[i][j] = 0
        else:
            New_Matrix[i][j] += Matrix[i][j]
            
print 'Original Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in Matrix]))     
print 'New Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in New_Matrix]))
#Find remaining paayments outside of friend groups   
for i in range(len(Matrix)):
    for j in range(len(Matrix)):
        if New_Matrix[i][j] == 0 and Matrix[i][j] != New_Matrix[i][j]:
            New_Matrix[i][j] = -1
            
print 'New Matrix'    
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in New_Matrix]))
          
