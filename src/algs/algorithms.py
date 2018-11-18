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
