import sys
sys.path.append("..")
import simulator
from collections import defaultdict

class OnlineWeightMatchingAlgorithm:
    """
    This is the abstract class that should be extended by any particular
    instance of an algorithm we want to test.

    The point is to define an API and some simple processes related to it.

    """
    def __init__(self):
        raise NotImplementedError

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
        raise NotImplementedError

class Greedy(OnlineWeightMatchingAlgorithm):
    # See algorithm 1.
    def __init__(self):
        self.p = defaultdict(float)
        # p from the algorithm is something like value
        # self.p is seller_index -> to -> value
        self.m = dict() # matches (index)
        # self.m is seller_index -> to -> matched_buyer_index

    def compute_matching(self, sim):
        matchings = []
        for node_index in range(sim.n + 1):
            assert sim.G.nodes[node_index]['in_market']
            if node_index in sim.seller_nodes:
                if sim.is_critical(node_index) and node_index in self.m:
                    matchings.append((node_index, self.m[node_index]))
            else:
                s, v_is = self.argmax(node_index, sim)
                if v_is - self.p[s] > 0:
                    self.m[s] = node_index
                    self.p[s] = v_is
        return matchings

    def argmax(self, b, sim):
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

class DynamicDeferredAcceptance(OnlineWeightMatchingAlgorithm):
    def __init__(self):
        pass

class BatchingAlgorithm(OnlineWeightMatchingAlgorithm):
    def __init__(
            self,
            max_weight_matching=Greedy(),
            batch=5):
        self.max_weight_alg = max_weight_matching
        self.batch = batch # make this d + 1

    def compute_matching(self, sim):
        if sim.t % self.batch == 0:
            return self.max_weight_alg.compute_matching(sim)
        return []
