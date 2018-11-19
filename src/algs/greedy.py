import sys
sys.path.append("..")
from algs.algorithms import OnlineWeightMatchingAlgorithm
from collections import defaultdict

class Greedy(OnlineWeightMatchingAlgorithm):
    # See algorithm 1.
    def __init__(self):
        self.p = defaultdict(float)
        # p from the algorithm is something like value
        # self.p is seller_index -> to -> value
        self.m = dict() # matches (index)
        # self.m is seller_index -> to -> matched_buyer_index
        self.critical_at = 1
        # needed for batching.

    def compute_matching(self, sim):
        """
        Input:
          Current state of the market. (from simulator)

        Output:
          Matching: a list, of (buyer, seller) pairs.
            buyer and seller are indexes into sim.G for the appropriate node.

        """
        self._reset_internals()
        self._process_buyers(sim)
        return self._process_critical_sellers(sim)

    def _process_buyers(self, sim):
        """
        Go through all buyer nodes in arrival order, matching a buyer to the
        seller with the highest marginal value, if positive.
        """
        for node_index in range(sim.n + 1):
            # not iterating over buyers set because order matters
            if node_index not in sim.G.nodes: continue # node has been removed
            assert sim.G.nodes[node_index]['in_market']
            if node_index in sim.buyer_nodes:
                s, v_is = self._argmax(node_index, sim)
                if v_is - self.p[s] > 0:
                    self.m[s] = node_index
                    self.p[s] = v_is


    def _process_critical_sellers(self, sim):
        """
        Go through all seller nodes in arrival order, and make a matching for
        the sellers that are 'critical'

        Output:
          Matching: a list, of (buyer, seller) pairs.
            buyer and seller are indexes into sim.G for the appropriate node.

        """
        matchings_reversed = {} # buyer : seller
        for node_index in range(sim.n + 1):
            # not iterating over sellers set because order matters
            if node_index in sim.seller_nodes:
                if sim.is_critical(node_index, self.critical_at) and node_index in self.m:
                    matchings_reversed[self.m[node_index]] = node_index
        return [(buyer, seller) for buyer, seller in matchings_reversed.items()]

    def _reset_internals(self):
        self.p = defaultdict(float)
        self.m = dict()

    def _argmax(self, b, sim):
        best_s = -1
        max_weight = -100000
        for s in sim.seller_nodes:
            w = sim.G.edges[(b,s)]['weight']
            if w > max_weight:
                max_weight = w
                best_s = s
        return (best_s, max_weight)

# Note: not exploring PostponedGreedy because we assume all buyers, sellers predefined
