import sys
sys.path.append("..")
import simulator

class OnlineWeightMatchingAlgorithm:
    """
    This is the abstract class that should be extended by any particular
    instance of an algorithm we want to test.

    The point is to define an API and some simple processes related to it.

    Input:
      Current state of the market. (from simulator)
      - The market state may be different depending on the algorithm.
        - For example, the Greedy Algorithm (3.1) requires a bipartite
          constrained online graph, but it also has way of creating one... TODO

    Output:
      Matching (could be None, 1, or multiple)

    """
    def __init__(self):
        raise NotImplementedError

    def compute_matching(self, sim):
        """
        Input:
            Take in a reference to the simulator object.
        Return:
            List of matchings computed.
        """
        raise NotImplementedError


class PostponedGreedy(OnlineWeightMatchingAlgorithm):
    def __init__(self):
        pass

class DynamicDeferredAcceptance(OnlineWeightMatchingAlgorithm):
    def __init__(self):
        pass

class BatchingAlgorithm(OnlineWeightMatchingAlgorithm):
    def __init__(
            self,
            max_weight_matching=DynamicDeferredAcceptance(),
            batch=5):
        self.max_weight_alg = max_weight_matching
        self.batch = batch # make this d + 1

    def compute_matching(self, sim):
        if sim.t % self.batch == 0:
            return self.max_weight_alg.compute_matching(sim)
        return []
