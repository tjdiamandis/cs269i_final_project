import time
import sys
sys.path.append("..")
import algs
import simulator

def weight_function(buyer_pos, buyer_d, seller_pos, seller_d):
    bx, by = buyer_pos
    sx, sy = seller_pos
    return 1.0/((bx-sx)**2 + (by-sy)**2 + 1)

def simple_test_cases(some_alg, verbose=False):
    A = time.time()
    total_value = 0
    sim = simulator.Simulator(weight_function)
    sim.add_node(pos=(0,0), d=5, k=0, buyer=True)
    sim.add_node(pos=(1,1), d=2, k=0, buyer=False)
    sim.add_node(pos=(0,0), d=2, k=3, buyer=False)
    max_steps = 5
    for t in range(max_steps):
        #print("Step %d" %t)
        crit_match = some_alg.compute_matching(sim)
        #print(crit_match)
        for match in crit_match:
            assert match[0] in sim.buyer_nodes
            total_value += sim.G[match[0]][match[1]]['weight']
            sim.remove_matching(match[0],match[1])
        sim.advance()
    print(total_value)
    if verbose:
        B = time.time()
        print("  1. First test completed in {} sec.".format(B - A))
        A = B

def test_greedy():
    print("Greedy Tests")
    A = time.time()
    simple_test_cases(algs.greedy.Greedy())
    print("Greedy tests completed successfully in {} sec".format(time.time() - A))


def test_dfa():
    print("DFA Tests")
    A = time.time()
    simple_test_cases(algs.deferred.DynamicDeferredAcceptance())
    print(
        "DynamicDeferredAcceptance tests completed successfully in {} sec".format(
            time.time() - A)
    )


def test_dla():
    print("DLA Tests")
    A = time.time()
    simple_test_cases(algs.lookahead.DeferredWithLookAhead(5))
    print(
        "DeferredWithLookAhead tests completed successfully in {} sec".format(
            time.time() - A)
    )

def test_all():
    test_greedy()
    test_dfa()
    test_dla()


if __name__ == "__main__":
    test_all()
