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
- REMOVE_MATCHING
  - when algorithm computes a list of matchings to create, we must remove them
    from the graph

Questions:
- Should only one node come on at each time step?
	- With departure times ticking down, this seems to inhibit flexibility
- What other things do algs need?
************************************************************************
"""


class Simulator:
	"""Simulates Ride Sharing Market

	The market is represented as a bipartite NetworkX graph
	- Nodes are either buyers or sellers
	- weights are calculated between the nodes as a function of position and
	  departure time of both nodes

	Instance variables:
		t  			: current timestep (starts at 0)
		n  			: index of last added node (starts at -1)
		G  			: graph containing state of market (access this for running algorithms)
		weight_func : weight function for caluclating edge weights
		buyer_nodes : list of buyer nodes in market
		seller_nodes: list of seller noes in market

	Functions:
		__init__ : initializes
		reset  	 : reset the graph.
		add_node : adds a node to the graph with a given position & departure time
		advance  : advances the market forward one step in time
		print_all: see what's going on (nodes, edges, who is buying, who is selling, etc)
	 ** Refer to individual function documentation for more information **

	Simulation:
	1. Initialtize the simulator:
		sim = simulator(N, weight_func)
	2. At each time step
		i. Add node:
			sim.add_node(pos_tuple, dep_time)
		ii. Run algorithms to fulfill your heart's desire
		iii. Advance time t -> t+1
			sim.advance(update_weights=False)

	Timer Mechanics:
	Ex. I add a node x at time t = 1 with d = 2
		- time 1: x.d = 2
		- advance()
		- time 2: x.d = 1
		- advance() # Removes x from market
		- time 3: x no longer in market

	Ex. I add a node x at time t = 1 with k = 2, d = 1
		- time 1: x.k = 2, x.d = 1
		- advance()
		- time 2: x.k = 1, x.d = 1
		- advance() # Places x into market
		- time 3: x.k = 0, x.d = 1  (x in market)
		- advance() # Removes x from market
		- time 4: x no longer in market

	See test_sim.py for usage examples
    """

	def __init__(self, weight_func):
		"""initializes instance of market

		Args:
			weight_func (function)	: function specifying how pairwise weights should be calculated
			  * Expected form of weight_func: weight_func(buyer_pos, buyer_d, seller_pos, seller_d)
		"""
		self.t = 0							# time step
		self.n = -1	 						# index of last added node
		self.G = nx.Graph()					# graph
		self.weight_func = weight_func		# weight function
		self.buyer_nodes = set()			# list of buyer nodes
		self.seller_nodes = set()			# list of seller nodes

	def reset(self):
		"""
		Resets everything except for the weight function
		"""
		self.t = 0
		self.n = -1
		self.G.clear()
		self.buyer_nodes.clear()
		self.seller_nodes.clear()

	def add_node(self, pos, d, buyer, k=0):
		"""Adds node to the market (buyer or seller)

		Args:
			pos (tup: (dbl, dbl)) : (x,y) position of node
			d (int)		  		  : number of advances until node exits market (rmvd. on d'th advance)
			buyer (bool)          : True = buyer, False = seller
			k (int)				  : steps to wait until node added to market (see ex in class desc)
		"""

		# Update node counter
		self.n += 1

		# Flags node if not yet present (in future state of market), but still adds edges
		in_market = False if k > 0 else True

		# Add node n and add edges to all other nodes based on weight_fun
		self.G.add_node(self.n, pos=pos, d=d, buyer=buyer, in_market=in_market, k=k)
		nodes_to_connect = self.seller_nodes if buyer else self.buyer_nodes

		for node in nodes_to_connect:
			node_pos = self.G.nodes[node]['pos']
			node_d = self.G.nodes[node]['d']
			buyer_pos, buyer_d   = (pos, d) if buyer else (node_pos, node_d)
			seller_pos, seller_d = (node_pos, node_d) if buyer else (pos, d)
			self.G.add_edge(
				self.n,
				node,
				weight=self.weight_func(
					buyer_pos=buyer_pos,
					buyer_d=buyer_d,
					seller_pos=seller_pos,
					seller_d=seller_d
				)
			)

		# Keep track if new node is buyer or seller
		if buyer:
			self.buyer_nodes.add(self.n)
		else:
			self.seller_nodes.add(self.n)

	def remove_matching(self, match):
		"""
		Input:
		  match - (buyer, seller) pair
		Output:
		  weight of the match
		"""
		pass

	def advance(self, recalc_weights=False):
		"""Advances the market by one step in time
			- Decrements departure time counter of all nodes in market
				- Removes nodes where departure_time(node) = 0
			- Decrements wait time counter of all nodes yet to be added
				- Adds nodes where wait_time(node) = 0
			- Recalculates weights (if flag)

		Args:
			recalc_weights (bool): If true, recalculates all weights in graph
				after counter is decremented. Use if function of dep. times
		"""

		# Increment time counter
		self.t += 1

		# Update deadlines of all nodes (in market + to be added)
		nodes_to_remove = []
		for node in self.G.nodes.items():
			# Nodes in market:
			#  - decrements dep. timer
			#  - tags nodes for removal when departure timer equals 0
			if node[1]['in_market']:
				dep_time = node[1]['d']
				if dep_time > 1:
					node[1]['d'] -=1
				else:
					nodes_to_remove.append(node[0])
					self.buyer_nodes.discard(node[0])
					self.seller_nodes.discard(node[0])

			# Nodes not yet in market:
			#  - decrements wait timer
			#  - add to market when wait timer equals 0
			else:
				node[1]['k'] -= 1
				if node[1]['k'] < 1:
					node[1]['in_market'] = True

		# Removes nodes
		self.G.remove_nodes_from(nodes_to_remove)

		# Recalc weights if flagged
		#  Iterates over buyers' edges; buyers are not connected to other buyers
		if recalc_weights:
			for buyer in self.buyer_nodes:
				buyer_pos = self.G.nodes[buyer]['pos']
				buyer_d   = self.G.nodes[buyer]['d']
				for seller in self.G.neighbors(buyer):
					seller_pos = self.G.nodes[seller]['pos']
					seller_d   = self.G.nodes[seller]['d']
					new_weight = self.weight_func(
						buyer_pos=buyer_pos,
						buyer_d=buyer_d,
						seller_pos=seller_pos,
						seller_d=seller_d
					)
					self.G[buyer][seller]['weight'] = new_weight


	# Utility Functions
	def print_nodes(self):
		"""Prints nodes
		"""
		not_in_market = []

		print("Nodes in market: (total in market + to be added: {})".format(
			len(self.G.nodes)
		))
		for node in self.G.nodes.items():
			if node[1]['in_market']:
				print(node)
			else:
				not_in_market.append(node)

		if len(not_in_market) > 0:
			print("Nodes not yet in market: ({})".format(len(not_in_market)))
			for node in not_in_market:
				print(node)


	def print_edges(self):
		"""Prints edges
		"""
		not_in_market = []

		print("Edges in market: (total in market + to be added: {})".format(
			len(self.G.edges)
		))
		for edge in self.G.edges.items():
			nodes, attr = edge
			if self.G.nodes[nodes[0]]['in_market'] and self.G.nodes[nodes[1]]['in_market']:
				print(edge)
			else:
				not_in_market.append(edge)

		if len(not_in_market) > 0:
			print("Edges not yet in market: ({})".format(len(not_in_market)))
			for edge in not_in_market:
				print(edge)

	def print_all(self):
		"""Prints buyer and sellers, nodes & edges
		"""
		print("\nTimestep: ", str(self.t))
		print("Buyers: " + str(self.buyer_nodes))
		print("Sellers: " + str(self.seller_nodes))
		self.print_nodes()
		self.print_edges()


# ****************************************************************
# Needs: (DONE)
# ****************************************************************
# - Graph with weights ~ to some function of (distance, etc) [can be changed] - DONE
# - Distribution of departure times baked into model - DONE, specified outside
# - "Look ahead" - keep track of nodes yet to be added - DONE
# ****************************************************************
