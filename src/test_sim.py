from simulator import simulator


def weight_function(x,y):
	return abs(x-y)

N = 10

sim = simulator(N, weight_function)
sim.add_node((0,0),2)
print(sim.G.nodes.items())
sim.advance()
print(sim.G.nodes.items())
sim.advance()