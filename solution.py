
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonals = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]



# TODO: Update the unit list to add the new diagonal units
unitlist = row_units + column_units + square_units + diagonals


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
	"""Eliminate values using the naked twins strategy.

	The naked twins strategy says that if you have two or more unallocated boxes
	in a unit and there are only two digits that can go in those two boxes, then
	those two digits can be eliminated from the possible assignments of all other
	boxes in the same unit.

	Parameters
	----------
	values(dict)
		a dictionary of the form {'box_name': '123456789', ...}

	Returns
	-------
	dict
		The values dictionary with the naked twins eliminated from peers

	Notes
	-----
	Your solution can either process all pairs of naked twins from the input once,
	or it can continue processing pairs of naked twins until there are no such
	pairs remaining -- the project assistant test suite will accept either
	convention. However, it will not accept code that does not process all pairs
	of naked twins from the original input. (For example, if you start processing
	pairs of twins and eliminate another pair of twins before the second pair
	is processed then your code will fail the PA test suite.)

	The first convention is preferred for consistency with the other strategies,
	and because it is simpler (since the reduce_puzzle function already calls this
	strategy repeatedly).
	"""

	twins = []

	for unit in unitlist:

		new_twins = []

		for box1 in unit:
			for box2 in unit: 
				if box1 is not box2 and values[box1] == values[box2] and len(values[box1]) == 2:
					new_twins.append([box1, box2])


		if new_twins:
			twins.append(new_twins)
		else:
			twins.append(False)

	for unit, pair in zip(unitlist, twins):
		if pair:
			twinA = pair[0][0]
			twinB = pair[1][0]
			valueA = values[twinA][0]
			valueB = values[twinA][1]

			for box in unit:
				if box is not twinA and box is not twinB:
					values = assign_value(values, box, values[box].replace(valueA, ''))
					values = assign_value(values, box, values[box].replace(valueB, ''))
	return values


def eliminate(values):
	"""Apply the eliminate strategy to a Sudoku puzzle

	The eliminate strategy says that if a box has a value assigned, then none
	of the peers of that box can have the same value.

	Parameters
	----------
	values(dict)
		a dictionary of the form {'box_name': '123456789', ...}

	Returns
	-------
	dict
		The values dictionary with the assigned values eliminated from peers
	"""
	solved = [box for box in boxes if len(values[box]) == 1]
	empties = [box for box in boxes if len(values[box]) == 0]

	for empty in empties:
		values[empty] = '123456789'

	for box in solved:

		for peer in peers[box]:
			values = assign_value(values, peer, values[peer].replace(values[box], ''))

	return values


def only_choice(values):
	"""Apply the only choice strategy to a Sudoku puzzle

	The only choice strategy says that if only one box in a unit allows a certain
	digit, then that box must be assigned that digit.

	Parameters
	----------
	values(dict)
		a dictionary of the form {'box_name': '123456789', ...}

	Returns
	-------
	dict
		The values dictionary with all single-valued boxes assigned

	Notes
	-----
	You should be able to complete this function by copying your code from the classroom
	"""
	for unit in unitlist:
		for digit in '123456789':

			matches = []
			
			for box in unit:
				if digit in values[box]:
					matches.append(box)
				
			if len(matches) == 1:
				values = assign_value(values, matches[0], digit)

	return values


def reduce_puzzle(values):
	"""Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

	Parameters
	----------
	values(dict)
		a dictionary of the form {'box_name': '123456789', ...}

	Returns
	-------
	dict or False
		The values dictionary after continued application of the constraint strategies
		no longer produces any changes, or False if the puzzle is unsolvable 
	"""
	stalled = False

	while not stalled:

		start_values = dict(values)

		reduced_values = eliminate(values)
		reduced_values = only_choice(reduced_values)
		
		stalled = start_values == reduced_values

		empties = [box for box in boxes if len(values[box]) == 0]

		if empties:
			return False
	
	return values


def search(values):
	"""Apply depth first search to solve Sudoku puzzles in order to solve puzzles
	that cannot be solved by repeated reduction alone.
				
	Parameters
	----------
	values(dict)
		a dictionary of the form {'box_name': '123456789', ...}

	Returns
	-------
	dict or False
		The values dictionary with all boxes assigned or False

	Notes
	-----
	You should be able to complete this function by copying your code from the classroom
	and extending it to call the naked twins strategy.
	"""

	if values is False:
		return values

	values = reduce_puzzle(values)

	unsolved = [box for box in boxes if len(values[box]) > 1]

	if len(unsolved) == 0:
		return values
	
	start_box = unsolved[0]

	for digit in values[start_box]:
		new_values = values.copy()
		new_values[start_box] = digit
		attempt = search(new_values)
		
		if attempt:
			return attempt


def solve(grid):
	"""Find the solution to a Sudoku puzzle using search and constraint propagation

	Parameters
	----------
	grid(string)
		a string representing a sudoku grid.
		
		Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

	Returns
	-------
	dict or False
		The dictionary representation of the final sudoku grid or False if no solution exists.
	"""
	values = grid2values(grid)
	values = search(values)
	return values


if __name__ == "__main__":
	diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
	display(grid2values(diag_sudoku_grid))
	result = solve(diag_sudoku_grid)
	display(result)

	try:
		import PySudoku
		PySudoku.play(grid2values(diag_sudoku_grid), result, history)

	except SystemExit:
		pass
	except:
		print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
