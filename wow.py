# Test push 2
num = int(raw_input())

graph = []
friends = []

for i in range(num):
	friend = map(int, raw_input().split())
	friends.append(friend)
	edges = raw_input().split(" ")
	edges = dict(map(int, edge.split(",")) for edge in edges)
	graph.append(edges)

print graph
print friends

networth = [0 for x in range(num)]
for i in range(num):
	for node in graph[i]:
		if node != -1:
			networth[i] -= graph[i][node]
			networth[node] += graph[i][node]

print networth
