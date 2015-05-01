import copy

#define class of people for input
class Person:
	def __init__(self, friends, payments):
		self.friends = friends
		self.payments = payments

class Optimizer:
	def __init__(self,people):
		self.people = people

	#write function for updating new graph with optimal payments
	#based on greedy algorithm to minimize number of payments
	def make_payment(self, graph, networth, networth_dict, payer_index, receiver_index, payment):
		#define who is paying 
		amount_can_pay = networth[payer_index]
		payer = networth_dict[payer_index][1]
		amount_can_receive = networth[receiver_index]
		receiver = networth_dict[receiver_index][1]

		#update graph with correct payment amount
		graph[payer][receiver] = payment

		#update payer and receiver to reflect payment made
		if payment == -(amount_can_pay):
			networth.pop(payer_index)
			networth_dict.pop(payer_index)
			if receiver_index != -1:
				receiver_index -= 1
		else:
			networth[payer_index] += payment
			networth_dict[payer_index] = (networth[payer_index], payer)

		if payment == amount_can_receive:
			networth.pop(receiver_index)
			networth_dict.pop(receiver_index)
		else:
			networth[receiver_index] -= payment
			networth_dict[receiver_index] = (networth[receiver_index], receiver)
		return

	def optimize(self):
		#read in all people
		
		people=self.people
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

		#print "original graph:"
		#print graph

		#initialize new graph for optimization
		new_graph = copy.deepcopy(graph)



		#update the graph for each unique friend group
		groups = len(friends)
		for i in range(groups):
			#initialize net worth list and list of index and net worth
			networth = [0 for x in range(num)]
			networth_indexes = [0 for x in range(num)]
			#clear all existing payments within friend group and add them to net worth
			for friend in friends[i]:
				for j in range(num):
					if new_graph[friend][j] != 0:
						networth[friend] -= new_graph[friend][j]
						networth[j] += new_graph[friend][j]
						new_graph[friend][j] = 0
			for k in range(num):
				networth_indexes[k] = (networth[k],k)

			#now order the networths so we can easily run the greedy algorithm
			ordered_networths = sorted(networth)
			ordered_networths_indexes = sorted(networth_indexes)
			ordered_networths = [x for x in ordered_networths if x != 0]
			ordered_networths_indexes = [x for x in ordered_networths_indexes if x[0] != 0]

			#begin greedy algorithm
			while ordered_networths != []:
				#reorder the networths on each run of the loop
				ordered_networths = sorted(ordered_networths)
				ordered_networths_indexes = sorted(ordered_networths_indexes)

				#if amount owed is larger than amount required for any one person, find if any perfect matches exist
				#otherwise, simply match largest amount owed to largest amount required
				if (ordered_networths[0] + ordered_networths[-1]) < 0:
					#search for perfect matches
					for l in range(1,len(ordered_networths)-1):
						#if we find a perfect match, use it (because this is optimal)
						if ordered_networths[l] + ordered_networths[-1] == 0:
							self.make_payment(new_graph, ordered_networths, ordered_networths_indexes, l, -1, ordered_networths[-1])
							break
						#else if we ever find that amount required is larger than amount owed, there's no perfect match
						elif ordered_networths[l] + ordered_networths[-1] > 0:
							self.make_payment(new_graph, ordered_networths, ordered_networths_indexes, 0, -1, ordered_networths[-1])
							break
						#otherwise, if we've gone through all options, match largest to largest
						else:
							if l == (len(ordered_networths) - 2):
								self.make_payment(new_graph, ordered_networths, ordered_networths_indexes, 0, -1, ordered_networths[-1])

				#if amount required is larger than amount owed for any one person, find if any perfect matches exist
				#otherwise, simply match largest amount owed to largest amount required
				elif (ordered_networths[0] + ordered_networths[-1] > 0):
					#search for perfect matches
					for l in reversed(range(1, len(ordered_networths)-1)):
						#if we find a perfect match, use it
						if ordered_networths[0] + ordered_networths[l] == 0:
							self.make_payment(new_graph, ordered_networths, ordered_networths_indexes, 0, l, ordered_networths[l])
							break
						#else if we ever find that amount owed is larger than amount required, there's no perfect match
						elif ordered_networths[0] + ordered_networths[l] < 0:
							self.make_payment(new_graph, ordered_networths, ordered_networths_indexes, 0, -1, -(ordered_networths[0]))
							break
						#otherwise, if we've gone through all options, match largest to largest
						else:
							if l == 1:
								self.make_payment(new_graph, ordered_networths, ordered_networths_indexes, 0, -1, -(ordered_networths[0]))

				#if a perfect match exists, use it
				else:
					self.make_payment(new_graph, ordered_networths, ordered_networths_indexes, 0, -1, -(ordered_networths[0]))

			#print "new graph", i+1, ":"
			#print new_graph
		return new_graph


Optimizer([Person([1,2,3], [(4,10),(2,20)]), Person([0,2,3], [(4,15),(5,20)]), Person([0,1,3], [(1,5),(6,10)]), Person([0,1,2],[(6,10)]), Person([5,6],[(5,10)]), Person([4,6],[]), Person([4,5],[])]).optimize()