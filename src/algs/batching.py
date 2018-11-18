from algs.algorithms import OnlineWeightMatchingAlgorithm

class BatchingAlgorithm(OnlineWeightMatchingAlgorithm):
    def __init__(
            self,
            max_weight_matching,
            batch=5):
        self.max_weight_alg = max_weight_matching
        self.batch = batch # make this d + 1

    def compute_matching(self, sim):
        if sim.t % self.batch == 0:
            return self.max_weight_alg.compute_matching(sim)
        return []
