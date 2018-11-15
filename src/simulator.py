import networkx as nx


class simulator:
	"""Simulates Ride Sharing Market

    """

	def __init__(self, N, weight_func):
		self.t = 0							# time step
		self.n = -1	 						# number of nodes we have added tot.
		self.N = N 							# total number of nodes
		self.G = nx.Graph()					# graph

	def add_node(self, pos, dep_time):
		# Update node counter
		#	Should equal current time step (add node t at time t)
		self.n += 1
		if not (self.n == self.t):
			print("WARNING: at time {}, but node {} added"
					.format(self.t,self.n))

		# Add node n and add edges to all other nodes based on weight_fun
		self.G.add_node(self.n, pos=pos, d=dep_time)
		for node in self.G.nodes.items():
			if not (node[0] == self.t):
				self.G.add_edge(self.t, node, weight=
								self.weight_func(node.pos, pos))


	def advance(self):
		# Increment time counter
		self.t += 1

		# Update deadlines of nodes in the market
		nodes_to_remove = []
		for node in self.G.nodes.items():
			# Tags nodes for removal when departure timer goes to 0
			dep_time = node[1]['d']
			if dep_time > 1:
				node[1]['d'] -=1
			else:
				nodes_to_remove.append(node[0])

		# Removes nodes
		self.G.remove_nodes_from(nodes_to_remove)



# Needs:
# - Graph with weights ~ to some function of (distance, etc) [can be changed]
# - Distribution of departure times baked into model
# - "Look ahead" - keep track of nodes yet to be added
# 	-- queue of nodes to be added of length look_ahead_n
