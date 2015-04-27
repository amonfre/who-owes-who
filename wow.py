import copy

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
#print friends

new_graph = copy.deepcopy(graph)
networth = [0 for x in range(num)]
networth_dict = [0 for x in range(num)]
for i in range(len(friends)):
	for friend in friends[i]:
		for j in range(num):
			if new_graph[friend][j] != 0:
				networth[friend] -= new_graph[friend][j]
				networth[j] += new_graph[friend][j]
				new_graph[friend][j] = 0
for i in range(num):
	networth_dict[i] = {networth[i]:i}

#print networth
#print networth_dict

ordered_networths = sorted(networth)
ordered_networths_dict = sorted(networth_dict)

#print ordered_networths
#print ordered_networths_dict

while ordered_networths != []:
	ordered_networths = sorted(ordered_networths)
	ordered_networths_dict = sorted(ordered_networths_dict)
	if (ordered_networths[0] + ordered_networths[-1]) < 0:
		for i in range(1,len(ordered_networths)-1):
			if ordered_networths[i] + ordered_networths[-1] == 0:
				new_graph[ordered_networths_dict[i][ordered_networths[i]]] \
				[ordered_networths_dict[-1][ordered_networths[-1]]] = ordered_networths[-1]
				ordered_networths.pop(i)
				ordered_networths.pop()
				ordered_networths_dict.pop(i)
				ordered_networths_dict.pop()
				break
			elif ordered_networths[i] + ordered_networths[-1] > 0:
				new_graph[ordered_networths_dict[0][ordered_networths[0]]] \
				[ordered_networths_dict[-1][ordered_networths[-1]]] = ordered_networths[-1]
				value = ordered_networths_dict[0][ordered_networths[0]]
				ordered_networths[0] = ordered_networths[0] + ordered_networths[-1]
				ordered_networths.pop()
				ordered_networths_dict[0] = {ordered_networths[0]:value}
				ordered_networths_dict.pop()
				break
			else:
				if i == (len(ordered_networths) - 2):
					new_graph[ordered_networths_dict[0][ordered_networths[0]]] \
					[ordered_networths_dict[-1][ordered_networths[-1]]] = ordered_networths[-1]
					value = ordered_networths_dict[0][ordered_networths[0]]
					ordered_networths[0] = ordered_networths[0] + ordered_networths[-1]
					ordered_networths.pop()
					ordered_networths_dict[0] = {ordered_networths[0]:value}
					ordered_networths_dict.pop()

	elif (ordered_networths[0] + ordered_networths[-1] > 0):
		for i in reversed(range(1, len(ordered_networths)-1)):
			if ordered_networths[0] + ordered_networths[i] == 0:
				new_graph[ordered_networths_dict[0][ordered_networths[0]]] \
				[ordered_networths_dict[i][ordered_networths[i]]] = ordered_networths[i]
				ordered_networths.pop(i)
				ordered_networths.pop(0)
				ordered_networths_dict.pop(i)
				ordered_networths_dict.pop(0)
				break
			elif ordered_networths[0] + ordered_networths[i] < 0:
				new_graph[ordered_networths_dict[0][ordered_networths[0]]] \
				[ordered_networths_dict[-1][ordered_networths[-1]]] = -(ordered_networths[0])
				value = ordered_networths_dict[-1][ordered_networths[-1]]
				ordered_networths[-1] = ordered_networths[0] + ordered_networths[-1]
				ordered_networths.pop(0)
				ordered_networths_dict[-1] = {ordered_networths[-1]:value}
				ordered_networths_dict.pop(0)
				break
			else:
				if i == 1:
					new_graph[ordered_networths_dict[0][ordered_networths[0]]] \
					[ordered_networths_dict[-1][ordered_networths[-1]]] = -(ordered_networths[0])
					value = ordered_networths_dict[-1][ordered_networths[-1]]
					ordered_networths[-1] = ordered_networths[0] + ordered_networths[-1]
					ordered_networths.pop(0)
					ordered_networths_dict[-1] = {ordered_networths[-1]:value}
					ordered_networths_dict.pop(0)

	else:
		new_graph[ordered_networths_dict[0][ordered_networths[0]]] \
		[ordered_networths_dict[-1][ordered_networths[-1]]] = ordered_networths[-1]
		ordered_networths.pop()
		ordered_networths.pop(0)
		ordered_networths_dict.pop()
		ordered_networths_dict.pop(0)

print new_graph


