from collections import defaultdict
from algs.algorithms import OnlineWeightMatchingAlgorithm

class DynamicDeferredAcceptance(OnlineWeightMatchingAlgorithm):
    # See algorithm 4.
    def __init__(self):
        self.price_s = defaultdict(float)
        # p from the algorithm is something like value
        # self.price_s is seller_index -> to -> value
        self.matching_s = dict() # matches (index)
        # self.matching_s is seller_index -> to -> matched_buyer_index
        self.marginal_profit_b = defaultdict(float)
        # self.marginal_profit_b q_b from the algorithm. For each buyer->seller
        # match made
        self.eps = 1e-3
        # for the ascending auction to ensure termination
        # Algorithmic analysis in the paper was conducted with self.eps -> 0

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
        Go through all buyer nodes in arrival order, conducting an ascending
        auction to create a tentative seller, buyer match.
        """
        for node_index in range(sim.n + 1):
            # not iterating over buyers set because order matters
            assert sim.G.nodes[node_index]['in_market']
            if node_index in sim.buyer_nodes:
                self._conduct_ascending_auction(sim, node_index)

    def _conduct_ascending_auction(self, sim, node_index):
        terminate = False
        b = node_index
        while not terminate:
            s, self.marginal_profit_b[b] = self._argmax(b, sim)
            if self.marginal_profit_b[b] > 0:
                prev_b = None
                if s in self.matching_s:
                    prev_b = self.matching_s[s]
                self.matching_s[s] = b
                self.price_s[s] += self.eps
                b = prev_b
            terminate = (b is None or self.marginal_profit_b[b] <= 0)

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
                if sim.is_critical(node_index) and node_index in self.matching_s:
                    matchings_reversed[self.matching_s[node_index]] = node_index
        return [(buyer, seller) for buyer, seller in matchings_reversed.items()]

    def _reset_internals(self):
        self.price_s = defaultdict(float)
        self.matching_s = dict()
        self.marginal_profit_b = defaultdict(float)

    def _argmax(self, b, sim):
        best_s = -1
        max_profit = -100000
        for s in sim.seller_nodes:
            v_bs = sim.G.edges[(b, s)]['weight']
            profit = v_bs - self.price_s[s]
            if profit > max_profit:
                max_profit = profit
                best_s = s
        return (best_s, max_profit)
