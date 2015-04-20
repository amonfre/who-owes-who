<<<<<<< HEAD
# Test push 2
=======
>>>>>>> 4f9df18c039e465276498212173237bf9482990f
num = int(raw_input())

graph = []
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
	edges = dict(map(int, edge.split(",")) for edge in edges)
	graph.append(edges)

print graph
print friends

networth = [0 for x in range(num)]
for i in range(len(friends)):
	for friend in friends[i]:
		for node in graph[friend]:
			networth[friend] -= graph[friend][node]
			networth[node] += graph[friend][node]

print networth
