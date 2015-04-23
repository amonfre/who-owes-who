num = int(raw_input())

graph = [[0 for x in range(num)] for y in range(num)]
friends = []

for i in range(num):
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
			graph[i][edge_value[0]] = edge_value[1]

print graph
print friends

networth = [0 for x in range(num)]
for i in range(len(friends)):
	for friend in friends[i]:
		for j in range(num):
			if graph[friend][j] != -1:
				networth[friend] -= graph[friend][j]
				networth[j] += graph[friend][j]

print networth