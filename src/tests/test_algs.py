import time
import sys
sys.path.append("..")
import algs

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

def test_all():
    test_abstract()


if __name__ == "__main__":
	test_all()
