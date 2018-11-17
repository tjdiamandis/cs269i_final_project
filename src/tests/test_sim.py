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

def main():
	# basic_tests()
	# test_dynamic_weights()
	test_look_ahead()



# Basic functionality
def basic_tests():
	# Test functionality without look ahead
	#  - Use a distance squared weight function
	def weight_function(buyer_pos, buyer_d, seller_pos, seller_d):
		bx, by = buyer_pos
		sx, sy = seller_pos
		return (bx-sx)**2 + (by-sy)**2


	# Test adding nodes and edges, timeout after d steps
	sim = simulator(weight_function)
	sim.add_node(pos=(0,0), d=2, buyer=True)
	sim.add_node(pos=(1,1), d=2, buyer=False)
	sim.print_all()
	sim.advance()
	sim.print_all()
	sim.advance()
	sim.print_all()
	sim.advance()
	sim.print_all()
	sim.add_node(pos=(0,0), d=1, buyer=True)
	sim.add_node(pos=(1,1), d=1, buyer=False)
	sim.add_node(pos=(-1,1), d=1, buyer=False)
	sim.add_node(pos=(-1,-1), d=1, buyer=True)
	sim.add_node(pos=(-1,-1), d=1, buyer=True)
	sim.print_all()
	sim.advance()
	sim.print_all()



# Test for when we want to update weights based on departure time
def test_dynamic_weights():
	
	# Use a distance squared weight function with dependence on buyer's departure time
	def weight_function_d(buyer_pos, buyer_d, seller_pos, seller_d):
		bx, by = buyer_pos
		sx, sy = seller_pos
		return ((bx-sx)**2 + (by-sy)**2) / buyer_d / seller_d

	# Test recalculating weight function (function of dep. time)
	sim = simulator(weight_function_d)
	sim.print_all()
	sim.add_node(pos=(0,0), d=2, buyer=True)
	sim.add_node(pos=(1,1), d=2, buyer=False)
	sim.print_all()
	sim.advance(recalc_weights=True)
	sim.print_all()
	sim.advance(recalc_weights=True)
	sim.print_all()
	sim.add_node(pos=(0,0), d=2, buyer=True)
	sim.add_node(pos=(1,1), d=2, buyer=False)
	sim.add_node(pos=(-1,1), d=2, buyer=False)
	sim.add_node(pos=(-1,-1), d=2, buyer=True)
	sim.add_node(pos=(-1,-1), d=2, buyer=True)
	sim.print_all()
	sim.advance(recalc_weights=True)
	sim.print_all()


# Test for basic look ahead functionality
def test_look_ahead():
	
	# Use a distance squared weight function with dependence on buyer's departure time
	def weight_function_d(buyer_pos, buyer_d, seller_pos, seller_d):
		bx, by = buyer_pos
		sx, sy = seller_pos
		return ((bx-sx)**2 + (by-sy)**2) / buyer_d / seller_d

	# Test recalculating weight function (function of dep. time)
	sim = simulator(weight_function_d)
	sim.print_all()
	sim.add_node(pos=(0,0), d=3, buyer=True, k=1)
	sim.add_node(pos=(1,1), d=3, buyer=False, k=2)
	sim.print_all()
	sim.advance(recalc_weights=True)
	sim.print_all()
	sim.advance(recalc_weights=True)
	sim.print_all()	
	sim.advance(recalc_weights=True)
	sim.print_all()	
	sim.advance(recalc_weights=True)
	sim.print_all()	



if __name__ == "__main__":
	main()

