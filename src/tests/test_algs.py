import time
import sys
sys.path.append("..")
import algs
import simulator

def test_abstract():
    A = time.time()
    try:
        algs.algorithms.OnlineWeightMatchingAlgorithm()
    except NotImplementedError:
        B = time.time()
        print("Abstract tests completed successfully in {} sec".format(B - A))
        return
    raise ValueError(
        "Algorithm Abstract Class initializes but should raise a NotImplementedError.")

def weight_function(buyer_pos, buyer_d, seller_pos, seller_d):
    bx, by = buyer_pos
    sx, sy = seller_pos
    return 1/((bx-sx)**2 + (by-sy)**2 + 1)

def make_default_sim():
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=True)
    sim.add_node(pos=(1,1), d=2, buyer=False)
    return sim

def test_greedy():
    A = time.time()
    greedy = algs.greedy.Greedy()
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=True)
    sim.add_node(pos=(1,1), d=2, buyer=False)
    sim.print_all()
    assert [] == greedy.compute_matching(sim)
    sim.advance()
    assert [(1,0)] == greedy.compute_matching(sim)
    # reverse order
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=False)
    sim.add_node(pos=(1,1), d=2, buyer=True)
    assert [] == greedy.compute_matching(sim)
    sim.advance()
    assert [(0,1)] == greedy.compute_matching(sim)
    # test only add one
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=1, buyer=False)
    sim.add_node(pos=(0,0), d=1, buyer=True)
    sim.add_node(pos=(1,1), d=1, buyer=True)
    assert [(0,1)] == greedy.compute_matching(sim)
    # test two matchings
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=1, buyer=False)
    sim.add_node(pos=(0,0), d=1, buyer=True)
    sim.add_node(pos=(1,1), d=1, buyer=True)
    sim.add_node(pos=(1,1), d=1, buyer=False)
    print(greedy.compute_matching(sim))
    assert [(0,1),(3,2)] == greedy.compute_matching(sim)
    # test two matchings, where a third node is best and shows up at end
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=False)
    sim.add_node(pos=(0,0), d=2, buyer=True)
    sim.add_node(pos=(1,1), d=2, buyer=True)
    sim.add_node(pos=(2,2), d=2, buyer=False)
    assert [] == greedy.compute_matching(sim)
    sim.advance()
    sim.add_node(pos=(1,1), d=1, buyer=False)
    print(greedy.compute_matching(sim))
    assert [(0,1),(4,2)] == greedy.compute_matching(sim)
    # test two matchings, third is best, but a new buyer
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=2, buyer=False)
    sim.add_node(pos=(0,0), d=2, buyer=True)
    sim.add_node(pos=(1,1), d=2, buyer=True)
    sim.add_node(pos=(2,2), d=2, buyer=False)
    assert [] == greedy.compute_matching(sim)
    sim.advance()
    sim.add_node(pos=(2,2), d=1, buyer=True)
    print(greedy.compute_matching(sim))
    assert [(0,1),(3,4)] == greedy.compute_matching(sim)
    sim.print_all()

def test_all():
    test_abstract()
    test_greedy()


if __name__ == "__main__":
    test_all()
