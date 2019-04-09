# Sudoku Solver
Part of Udacity's Artificial Intelligence Nanodegree, the following code can be used to solve sudokus using multiple methods of elimination in combination. In this project, I extended the Sudoku-solving agent developed in the classroom lectures to solve _diagonal_ Sudoku puzzles and implement a new constraint strategy called "naked twins". 

A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks). The naked twins strategy says that if you have two or more unallocated boxes in a unit and there are only two digits that can go in those two boxes, then those two digits can be eliminated from the possible assignments of all other boxes in the same unit.


## Solution

### Naked Twins

Eliminate values using the naked twins strategy.
  The naked twins strategy says that if you have two or more unallocated boxes
  in a unit and there are only two digits that can go in those two boxes, then
  those two digits can be eliminated from the possible assignments of all other
  boxes in the same unit.
  
  Parameters:
  values(dict)
    a dictionary of the form {'box_name': '123456789', ...}
  
  Returns:
  dict
    The values dictionary with the naked twins eliminated from peers

```python
def naked_twins(values):

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
```

### Elimination Strategy

  Apply the eliminate strategy to a Sudoku puzzle
  The eliminate strategy says that if a box has a value assigned, then none
  of the peers of that box can have the same value.
  
  Parameters:
  values(dict)
    a dictionary of the form {'box_name': '123456789', ...}
  Returns

  dict:
    The values dictionary with the assigned values eliminated from peers

```python
def eliminate(values):

  solved = [box for box in boxes if len(values[box]) == 1]
  empties = [box for box in boxes if len(values[box]) == 0]

  for empty in empties:
    values[empty] = '123456789'

  for box in solved:

    for peer in peers[box]:
      values = assign_value(values, peer, values[peer].replace(values[box], ''))

  return values
```

### Only Choice
Apply the only choice strategy to a Sudoku puzzle
The only choice strategy says that if only one box in a unit allows a certain
digit, then that box must be assigned that digit.
	
Parameters:
	values(dict)
	a dictionary of the form {'box_name': '123456789', ...}

Returns:
dict
The values dictionary with all single-valued boxes assigned
Notes

```python
def only_choice(values):
  for unit in unitlist:
  for digit in '123456789':

  matches = []

  for box in unit:
  if digit in values[box]:
  matches.append(box)

  if len(matches) == 1:
  values = assign_value(values, matches[0], digit)

  return values
```
### Reduce Puzzle
Reduce a Sudoku puzzle by repeatedly applying all constraint strategies
	
Parameters:
	values(dict)
		a dictionary of the form {'box_name': '123456789', ...}
	
Returns:
	dict or False
		
   The values dictionary after continued application of the constraint strategies
		no longer produces any changes, or False if the puzzle is unsolvable 
        
```python
def reduce_puzzle(values):
	
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
```

### Search

Apply depth first search to solve Sudoku puzzles in order to solve puzzles
	that cannot be solved by repeated reduction alone.
				
Parameters:
	values(dict)
		a dictionary of the form {'box_name': '123456789', ...}

Returns: dict or False

The values dictionary with all boxes assigned or False
	
```python
def search(values):

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
```
