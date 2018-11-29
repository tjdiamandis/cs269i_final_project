import time
import sys
sys.path.append("..")
sys.path.append("../algs/")

import algs
import simulator

def test_abstract():
    A = time.time()
    try:
        algs.OnlineWeightMatchingAlgorithm()
    except NotImplementedError:
        B = time.time()
        print("Abstract tests completed successfully in {} sec.".format(B - A))
        return
    raise ValueError(
        "Algorithm Abstract Class initializes but should raise a NotImplementedError.")

def weight_function(buyer_pos, buyer_d, seller_pos, seller_d):
    bx, by = buyer_pos
    sx, sy = seller_pos
    return 1.0/((bx-sx)**2 + (by-sy)**2 + 1)

def simple_test_cases(some_alg, verbose=False):
    A = time.time()
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=True)
    sim.add_node(pos=(1,1), d=2, buyer=False)
    assert [] == some_alg.compute_matching(sim)
    sim.advance()
    assert [(0,1)] == some_alg.compute_matching(sim)
    if verbose:
        B = time.time()
        print("  1. First test completed in {} sec.".format(B - A))
        A = B
    # reverse order
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=False)
    sim.add_node(pos=(1,1), d=2, buyer=True)
    assert [] == some_alg.compute_matching(sim)
    sim.advance()
    assert [(1,0)] == some_alg.compute_matching(sim)
    if verbose:
        B = time.time()
        print("  2. Reverse simple test completed in {} sec.".format(B - A))
        A = B
    # test only add one
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=1, buyer=False)
    sim.add_node(pos=(0,0), d=1, buyer=True)
    sim.add_node(pos=(1,1), d=1, buyer=True)
    assert [(1,0)] == some_alg.compute_matching(sim)
    if verbose:
        B = time.time()
        print("  3. Choose only one match test completed in {} sec.".format(B - A))
        A = B
    # test two matchings
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=1, buyer=False)
    sim.add_node(pos=(0,0), d=1, buyer=True)
    sim.add_node(pos=(1,1), d=1, buyer=True)
    sim.add_node(pos=(1,1), d=1, buyer=False)
    assert [(1,0),(2,3)] == some_alg.compute_matching(sim)
    if verbose:
        B = time.time()
        print("  4. Two matchings test completed in {} sec.".format(B - A))
        A = B
    # test two matchings, where a third node is best and shows up at end
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=False)
    sim.add_node(pos=(0,0), d=2, buyer=True)
    sim.add_node(pos=(1,1), d=2, buyer=True)
    sim.add_node(pos=(2,2), d=2, buyer=False)
    assert [] == some_alg.compute_matching(sim)
    sim.advance()
    sim.add_node(pos=(1,1), d=1, buyer=False)
    assert [(1,0),(2,4)] == some_alg.compute_matching(sim)
    if verbose:
        B = time.time()
        print("  5. Only choose two test completed in {} sec.".format(B - A))
        A = B
    # test two matchings, third is best, but a new buyer
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=False)
    sim.add_node(pos=(0,0), d=2, buyer=True)
    sim.add_node(pos=(1,1), d=2, buyer=True)
    sim.add_node(pos=(2,2), d=2, buyer=False)
    assert [] == some_alg.compute_matching(sim)
    sim.advance()
    sim.add_node(pos=(2,2), d=1, buyer=True)
    assert [(1,0),(4,3)] == some_alg.compute_matching(sim)
    if verbose:
        B = time.time()
        print("  6. Only choose two - new buyer - test completed in {} sec.".format(B - A))
        A = B

def test_greedy():
    A = time.time()
    simple_test_cases(algs.Greedy())
    print("Greedy tests completed successfully in {} sec".format(time.time() - A))


def test_dfa():
    A = time.time()
    simple_test_cases(algs.DynamicDeferredAcceptance(), verbose = True)
    print(
        "DynamicDeferredAcceptance tests completed successfully in {} sec".format(
            time.time() - A)
    )

def test_batching():
    A = time.time()
    simple_test_cases(algs.BatchingAlgorithm(
        algs.greedy.Greedy(),
        batch=1)
    )
    print("Batched Greedy tests completed successfully in {} sec".format(time.time() - A))
    A = time.time()
    simple_test_cases(algs.BatchingAlgorithm(
        algs.deferred.DynamicDeferredAcceptance(),
        batch=1)
    )

    batch_alg = algs.BatchingAlgorithm(algs.greedy.Greedy(), batch=2)
    A = time.time()
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=True)
    sim.add_node(pos=(1,1), d=2, buyer=False)
    assert [(0,1)] == batch_alg.compute_matching(sim)
    print(
        "Batch != 1 Batched Greedy test completed successfully in {} sec".format(
            time.time() - A)
    )

def test_all():
    test_abstract()
    test_greedy()
    test_dfa()
    test_batching()


if __name__ == "__main__":
    test_all()
