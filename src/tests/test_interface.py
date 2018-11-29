import time
import sys
sys.path.append("..")
import interface
import simulator
import algs

# TODO all of these tests...
def test_interface():
    A = time.time()
    def weight_func(buyer_pos, buyer_d, seller_pos, seller_d):
        return abs(buyer_pos[0] - seller_pos[0])
    inter = interface.Interface(
        algs.Greedy(),
        simulator.Simulator(weight_func),
        seed=42,
        dep_distr=(3,0), # to make d constant for all nodes, make variance 0 (duh)
        verbose=True)
    inter.run(10)
    B = time.time()
    print("Interface tests completed successfully in {} sec".format(B - A))


if __name__ == "__main__":
	test_interface()
