from simulator import simulator

"""
************************************************************************
OPEN TODOS:
************************************************************************
TODO:
- Unit tests for all functionality

************************************************************************
"""


def weight_function(x,y):
	return abs(x-y)

N = 10

sim = simulator(N, weight_function)
sim.add_node((0,0),2, True)
sim.add_node((0,0),2, False)
print(sim.G.nodes.items())
sim.advance()
print(sim.G.nodes.items())
sim.advance()