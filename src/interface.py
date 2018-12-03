"""
This file serves as the interface between the simulator and the algorithms.
"""
import numpy as np


class Interface:
    """
    Use case:
      def conduct_experiments():
          interface = Interface(algorithm, simulator)
          weights_or_other_stats = []
          for i in range(num_experiments):
              weighting_found = interface.run(exp.num_steps)
              weights.append(weighting_found)
          plot(weights)
    """
    def __init__(
            self,
            algorithm,
            sim,
            p_node=0.2,
            min_to_add=1,
            max_to_add=1,
            p_buyer=0.5,
            size=(10,10),
            dep_distr=(3,1), # to make d constant for all nodes, make variance 0 (duh)
            seed=None,
            verbose=False
    ):
        self.max_weight_alg = algorithm
        self.sim = sim
        self.p_node = p_node
        self.min_to_add = min_to_add
        self.max_to_add = max_to_add
        self.p_buyer = p_buyer
        self.size = size
        self.d_mean = dep_distr[0]
        self.d_var = dep_distr[1]
        self.verbose = verbose
        if seed:
            np.random.seed(seed)
            if self.verbose: print("Random seed set to: ", seed)

    def run(self, num_steps):
        self.sim.reset()
        weights = []
        discarded_buyers = []
        discarded_sellers = []
        for i in range(num_steps):
            node_added = self._maybe_add_node(self.min_to_add, self.max_to_add)
            if node_added and self.verbose:
                print("Added a node at step ", i)
            matchings = self.max_weight_alg.compute_matching(self.sim)
            for match in matchings:
                weight = self.sim.remove_matching(match[0], match[1])
                weights.append((weight, i))
            removed_b, removed_s = self.sim.advance()
            discarded_buyers.append((removed_b, i))
            discarded_sellers.append((removed_s, i))
        return weights, discarded_buyers, discarded_sellers

    def _maybe_add_node(self, min_to_add, max_to_add):
        if np.random.randint(0,1) > self.p_node: return 0
        if min_to_add == max_to_add:
            num_to_add = min_to_add
        else:
            num_to_add = np.random.randint(min_to_add, max_to_add)
        if num_to_add == 0: return 0
        for i in range(num_to_add):
            pos_x = round(np.random.uniform(0, self.size[0]))
            pos_y = round(np.random.uniform(0, self.size[1]))
            d = max(round(np.random.normal(self.d_mean, self.d_var)), 1)
            is_buyer = True if np.random.uniform(0,1) <= self.p_buyer else False
            self.sim.add_node((pos_x, pos_y), d, is_buyer, k=0)
            if self.verbose:
                print("Node: ({},{}), {}, {}".format(pos_x,pos_y,d,is_buyer))
        return num_to_add
