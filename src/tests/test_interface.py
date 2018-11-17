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
        return 1
    interface.Interface(algs.PostponedGreedy(), simulator.Simulator(weight_func))
    B = time.time()
    print("Interface tests completed successfully in {} sec".format(B - A))


if __name__ == "__main__":
	test_interface()
