
from tests import test_sim, test_algs, test_interface

if __name__ == "__main__":
    print("Testing simulator")
    test_sim.main()

    print("\nTesting algorithms")
    test_algs.test_all()

    print("\nTesting interface")
    # BROKEN
    test_interface.test_interface()
