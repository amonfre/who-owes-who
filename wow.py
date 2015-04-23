num = int(raw_input())

graph = []
friends = []

for i in range(num):
	friend = map(int, raw_input().split())
	friends.append(friend)
	edges = raw_input().split(" ")
	edges = dict(edge.split(",") for edge in edges)
	graph.append(edges)

print graph
print friends

