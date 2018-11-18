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
            p_buyer=0.5,
            size=(10,10),
            dep_distr=(3,1), # to make d constant for all nodes, make variance 0 (duh)
            seed=None,
            verbose=False
    ):
        self.max_weight_alg = algorithm
        self.sim = sim
        self.p_node = p_node
        self.p_buyer = p_buyer
        self.size = size
        self.d_mean = dep_distr[0]
        self.d_var = dep_distr[1]
        self.verbose = verbose
        self.seed = seed
        if self.seed:
            np.random.seed(self.seed)
            if self.verbose: print("Random seed set to: ", self.seed)

    def run(self, num_steps):
        self.sim.reset()
        weights = []
        for i in range(num_steps):
            node_added = self._maybe_add_node()
            if node_added and verbose:
                print("Added a node at step ", i)
            matchings = self.algorithm.compute_matching(self.sim)
            for match in matchings:
                weights.append(self.sim.remove_matching(match))
            self.sim.advance() # includes adding a node?
        return weights

    def _maybe_add_node(self):
        if np.random.uniform(0,1) > self.p_node: return False
        pos_x = np.random.uniform(0, self.size[0])
        pos_y = np.random.uniform(0, self.size[1])
        d = round(np.random.normal(self.d_mean, self.d_var))
        is_buyer = True if np.random.uniform(0,1) <= self.p_buyer else False
        self.sim.add_node((pos_x, pos_y), d, is_buyer, k=0)
        return True