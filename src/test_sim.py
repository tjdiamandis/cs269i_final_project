from simulator import simulator

"""
************************************************************************
OPEN TODOS:
************************************************************************
TODO:
- Unit tests for all functionality
	- Testing...

************************************************************************
"""


# Use a distance squared weight function for simplicity in testing
def weight_function(buyer_pos, buyer_d, seller_pos, seller_d):
	bx, by = buyer_pos
	sx, sy = seller_pos
	return (bx-sx)**2 + (by-sy)**2

N = 10

sim = simulator(N, weight_function)
sim.add_node((0,0),2, True)
sim.add_node((0,0),2, False)
print(sim.G.nodes.items())
sim.advance()
print(sim.G.nodes.items())
sim.advance()

# Use a distance squared weight function with dependence on buyer's departure time
def weight_function_d(buyer_pos, buyer_d, seller_pos, seller_d):
	bx, by = buyer_pos
	sx, sy = seller_pos
	return ((bx-sx)**2 + (by-sy)**2) / buyer_d