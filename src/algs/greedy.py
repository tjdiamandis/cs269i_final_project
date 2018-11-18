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

    def compute_matching(self, sim):
        """
        Input:
          Current state of the market. (from simulator)
          - The market state may be different depending on the algorithm.
            - For example, the Greedy Algorithm (3.1) requires a bipartite
              constrained online graph, but it also has way of creating one... TODO

        Output:
          Matching: a list, of (buyer, seller) pairs.
            buyer and seller are indexes into sim.G for the appropriate node.

        """
        self._reset_internals()
        matchings_reversed = {} # buyer : seller
        for node_index in range(sim.n + 1):
            # not iterating over buyers because order matters
            assert sim.G.nodes[node_index]['in_market']
            if node_index in sim.buyer_nodes:
                s, v_is = self._argmax(node_index, sim)
                if v_is - self.p[s] > 0:
                    self.m[s] = node_index
                    self.p[s] = v_is
        for node_index in range(sim.n + 1):
            # not iterating over buyers because order matters
            if node_index in sim.seller_nodes:
                if sim.is_critical(node_index) and node_index in self.m:
                    matchings_reversed[self.m[node_index]] = node_index
        return [(seller, buyer) for buyer, seller in matchings_reversed.items()]

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


class PostponedGreedy(OnlineWeightMatchingAlgorithm):
    def __init__(self):
        pass
