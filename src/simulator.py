"""
Defines class to simulate ride sharing market
Last Modified: Nov 15, 2018

"""

import networkx as nx


"""
************************************************************************
OPEN TODOS:
************************************************************************
TODO:
- Update all weights in advance step
	- Iterate over nodes or over edges?

Questions:
- Should only one node come on at each time step?
	- With departure times ticking down, this seems to inhibit flexibility
- What other things do algs need?
************************************************************************
"""


class simulator:
	"""Simulates Ride Sharing Market

	The market is represented as a bipartite NetworkX graph
	- Nodes are either buyers or sellers
	- weights are calculated between the nodes as a function of position and 
		departure time of both nodes

	Instance variables:
		t  			: current timestep (starts at 0)
		n  			: index of last added node (starts at -1)
		N  			: total number of nodes -- MIGHT REMOVE THIS?
		G  			: graph containing state of market
		weight_func : weight function for caluclating edge weights 

	Functions:
		__init__ : initializes
		add_node : adds a node to the graph with a given position & dep. time
		advance  : advances the market forward one step in time


	Simulation:
	1. Initialtize the simulator:
		sim = simulator(N, weight_func)
	2. At each time step
		i. Add node:
			sim.add_node(pos_tuple, dep_time)
		ii. Advance time t -> t+1
			sim.advance(update_weights=False)

	Look at test_sim.py for usage examples

	Refer to individual function documentation for more information
    """

	def __init__(self, N, weight_func):
		"""initializes instance of market
		
		Args:
			N (int)  				: number of total nodes to be added 
			weight_func (function)	: function specifying how pairwise weights
									  should be calculated
				Expected form of weight_func:
					weight_func(buyer_pos, buyer_d, seller_pos, seller_d)
		"""
		self.t = 0							# time step
		self.n = -1	 						# index of last added node
		self.N = N 							# total number of nodes
		self.G = nx.Graph()					# graph
		self.weight_func = weight_func		# weight function
		self.buyer_nodes = []				# list of buyer nodes
		self.seller_nodes = [] 				# list of seller nodes


	def add_node(self, pos, dep_time, buyer):
		"""Adds node to the market (buyer or seller)
		
		Args:
			pos (tup: (dbl, dbl)) : (x,y) position of node
			dep_time (int)		  : number of advances until node leaves market
			buyer (bool)          : True = buyer, False = seller
		"""

		# Update node counter
		#	Should equal current time step (add node t at time t)
		self.n += 1
		if not (self.n == self.t):
			print("WARNING: at time {}, but node {} added"
					.format(self.t,self.n))

		# Add node n and add edges to all other nodes based on weight_fun
		self.G.add_node(self.n, pos=pos, d=dep_time, buyer=buyer)
		nodes_to_connect = self.seller_nodes if buyer else self.buyer_nodes

		for node in nodes_to_connect:
			buyer_pos, buyer_d   = (pos, dep_time)    if buyer else (node.pos, node.d)
			seller_pos, seller_d = (node.pos, node.d) if buyer else (pos, dep_time)
			self.G.add_edge(self.t, node, weight=
							self.weight_func(buyer_pos, buyer_d, seller_pos, seller_d))

		# Keep track if new node is buyer or seller
		if buyer: self.buyer_nodes.append(self.n) 
		else: self.seller_nodes.append(self.n)
				


	def advance(self, recalc_weights=False):
		"""Advances the market by one step in time
			- Decrements departure time counter of all nodes
			- Removes nodes where departure_time(node) = 0
			- Recalculates weights (if flag)
		
		Args:
			recalc_weights (bool): If true, recalculates all weights in graph
								   after counter is decremented
		"""

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

		# Recalc weights if flagged
		if recalc_weights:
			for edge in self.G.edges:
				print(edge)





# ****************************************************************
# Needs:
# ****************************************************************
# - Graph with weights ~ to some function of (distance, etc) [can be changed] - DONE
# - Distribution of departure times baked into model - DONE, specified outside
# - "Look ahead" - keep track of nodes yet to be added
# 	-- queue of nodes to be added of length look_ahead_n
# ****************************************************************
