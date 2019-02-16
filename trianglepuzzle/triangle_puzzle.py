'''
The triangle puzzle and solver.
'''

import numpy as np
from collections import defaultdict


class TrianglePuzzle:
    '''
    The objective of this puzzle is to find the path from the number at the
    top of the triangle all down to the bottom row such that the product of all
    the values visited is equal to the target number.

    This puzzle is set up such that the first row contains one positive
    integer, the second row contains two positive integers, and so on, creating
    a triangle. Starting from the initial position at the top of the triangle,
    the player continually moves down one row by moving to the value down and
    to the left of the current position, or down and to the right of the
    current position--until the player reaches the bottom row. In this way,
    the player visits the same number of values as there are rows in the
    triangle. The player must find the path that makes the product of all the
    values visited equal to the specified target value.

    Parameters
    ----------------------------------
    triangle : list of lists
        lists consist of positive integers and each list must be one item
        longer than the one previous
    target : int (positive)
        must define a unique path down the triangle

    Attributes
    ----------------------------------
    solution : str
        consisting of 'L' and 'R' specifying the steps that solve the puzzle.
    '''

    def __init__(self, triangle=None, target=None):
        self.triangle = triangle
        self.target = target
        self.solution_ = None

    def read_txt_file(self, text_file_path):
        '''
        Get the triangle from a text file.

        Parameters
        ----------------------------------
        text_file_path : str
            indicating the path to the text file

        Returns self
        '''
        puzzle = open(text_file_path, 'r').readlines()
        triangle = []
        for line in puzzle:
            if line[-1] == '\n':
                line = line[:-1]
            if line.strip()[0].isdigit():
                row = [int(s) for s in line.split(',') if s.isdigit()]
                triangle.append(row)
            else:
                target = [int(s) for s in line.split(' ') if s.isdigit()]

        # Check to make sure only 1 target in list
        if len(target) > 1:
            raise ValueError('More than one target was specified in the file.')
        elif len(target) < 1:
            raise ValueError('Could not find a target value in the file.')
        else:
            self.set_target(target[0])

        self.set_triangle(triangle)
        return self

    def set_triangle(self, triangle):
        '''
        Sets the triangle parameter of the puzzle and ensures it is in a valid
        form.

        Parameters
        ----------------------------------
        triangle : list of lists
            lists consist of positive integers and each list must be one item
            longer than the one previous

        Returns self
        '''
        for row, values in enumerate(triangle):
            if len(values) != row + 1:
                raise ValueError('The triangle is not the correct shape.')
            for value in values:
                try:
                    value = int(value)
                except ValueError:
                    print('Could not convert one or more values to an int.')
                    raise
        self.triangle = triangle
        return self

    def set_target(self, target):
        '''
        Sets the target parameter of the puzzle and ensures it is a positive
        int.

        Parameters
        ----------------------------------
        target : int
            must be positive

        Returns self
        '''
        try:
            self.target = int(target)
        except ValueError:
            print('Could not convert target value to an integer.')
        return self

    def solve(self):
        '''
        Generates the solution to the puzzle.

        Returns str : the solution to the puzzle consisting of 'L' and 'R'
        indicating taken as the solution.
        '''
        # Initiate tracker
        rows = len(self.triangle)
        tracker = TriangleSolutionTracker()

        value = self.triangle[tracker.current_row][tracker.current_position]
        current_target = self.target / value
        tracker._make_move(value=value)

        # If the value at the top of the triangle is not a factor of the
        # target, there is no solution to the puzzle, so raise an error
        if self.target % value != 0:
            raise ValueError('There is no solution to this puzzle.')

        else:
            while tracker.current_row <= rows:
                # If we've reached the final row
                if tracker.current_row == rows:
                    # If the puzzle has been solved, produce the output
                    if self.target == np.prod(tracker.values):
                        self.solution = ''.join(tracker.output)
                        return self.solution
                    # If we have not reached the target, backtrack
                    else:
                        current_target, tracker = self._backtrack(
                            tracker=tracker)
                        tracker.current_row -= 1

                # Determine next possible move
                else:
                    current_target, tracker = self._next_move(
                        current_target=current_target, tracker=tracker,
                        backtrack=False)

    def _next_move(self, tracker, current_target, backtrack=False):
        '''
        Helper function for self.solve(). Determines the next move to make.
        Checks if moving left will land on a value that is a factor of the
        current target. If true, updates TriangleSolutionTracker attributes.
        If false, does the same with moving right. If neither is a possibility,
        backtracks up the triangle.

        Returns current_target : int, tracker : TriangleSolutionTracker
        '''
        if not backtrack:
            valueL = self.triangle[tracker.current_row][
                tracker.current_position]
            # Check if we can move left
            if current_target % valueL == 0:
                # Update variables with values from move
                current_target = current_target / valueL
                tracker._make_move(value=valueL, direction='L')
                return current_target, tracker
            else:
                pass
        else:
            pass

        valueR = self.triangle[tracker.current_row][
            tracker.current_position + 1]
        # Check if we can move right
        if current_target % valueR == 0:
            # Update variables with values from move
            current_target = current_target / valueR
            tracker._make_move(value=valueR, direction='R')
        # If we could not make a move from the current position, backtrack up
        # the triangle.
        else:
            current_target, tracker = self._backtrack(tracker)
            tracker.current_row += 1
        return current_target, tracker

    def _backtrack(self, tracker):
        '''
        Helper function to self.solve(). When the solver hits a dead end,
        retraces steps to the first possible change.

        Returns current_target : int, tracker : TriangleSolutionTracker
        '''

        # The solution function will always try to move left before it tries
        # to move right, so if there are only moves to the right, we have
        # checked every possiblity, so raise an error
        if 'L' not in tracker.output:
            raise ValueError('There is no solution to this puzzle.')

        else:
            # Retrace moves up to most recent 'left' move.
            # Update necessary variables.
            while tracker.output.pop() == 'R':
                tracker.current_row -= 1
                tracker.current_position -= 1
                tracker.values.pop()
            tracker.values.pop()
            tracker.current_row -= 1

            product = np.prod(tracker.values)
            # Re-calculate current_target
            current_target = self.target / product
            current_target, tracker = self._next_move(
                tracker=tracker, current_target=current_target, backtrack=True)
        # Return
        return current_target, tracker

    def make_random(self, n_rows=5, level=None):
        '''
        Constructs a random triangle puzzle that has a single, valid solution.

        Parameters
        ----------------------------------
        n_rows : int
            a number between 2 and 12 inclusive
        level : str
            options are 'easy', 'medium', and 'hard'

        Returns self
        '''
        if n_rows >= 12:
            raise ValueError('The maximum number of rows allowed is 11.')
        if not level:
            max_value = 3 * n_rows
        else:
            assert level in set(['easy', 'medium', 'hard']),
            'Options for level are \'easy\', \'medium\', or \'hard\'.'
        elif level == 'easy':
            max_value = 2 * n_rows
        elif level == 'medium':
            max_value = 3 * n_rows
        else:
            max_value = 4 * n_rows

        values = list(range(2, (max_value + 1)))
        ratios = np.array(list(reversed(values)))
        probabilities = ratios / ratios.sum()

        self.triangle = []
        self.target = None
        valid = False
        while not valid:
            for i in range(n_rows):
                row = np.random.choice(values, size=(i + 1), p=probabilities)
                self.triangle.append(row)

            valid, targets = self._is_valid_puzzle()
        self.target = np.random.choice(targets)
        return self

    def _is_valid_puzzle(self):
        '''
        Checks that the puzzle is valid with a single, unique solution.

        Returns self, possible_targets : list of ints that could be valid
            targets to the puzzle.
        '''
        possible_products = defaultdict(int)
        n_moves = len(self.triangle) - 1
        paths = list(range(2 ** n_moves))
        for path in paths:
            moves = bin(path)[2:]
            while len(moves) < 4:
                moves = '0' + moves
            paths[path] = [int(move) for move in moves]
        for path in paths:
            values = [self.triangle[0][0]]
            for row in range(len(moves)):
                moves[row] = moves[row] + moves[row - 1]
                values.append(self.triangle[row + 1][moves[row]])
            product = np.prod(values)
            possible_products[product] += 1
        if self.target:
            if possible_products[str(self.target)] == 1:
                return True, self.target
            else:
                return False, None
        else:
            possible_targets = []
            for product, n in possible_products:
                if n == 1:
                    possible_targets.append(int(product))
            if len(possible_targets) == 0:
                return False, None
            else:
                return True, possible_targets


class TriangleSolutionTracker:
    '''
    Tracker to hold information regarding the state of the puzzle solver.

    Attributes
    ----------------------------------
    output : list
        list of type str ('L' and 'R') indicating moves taken by the solver in
        its current path.
    values : list
        list of type int indicating values visited along its current path
    current_position : int
    current_row : int
    '''

    def __init__(self):
        self.output = []
        self.values = []
        self.current_position = 0
        self.current_row = 0

    def _update(self, values=None, output=None,
                current_position=None, current_row=None):
        '''
        Function to update the parameters of the solution tracker.

        Returns self
        '''
        if values:
            self.values = values
        if output:
            self.output = output
        if current_position:
            self.current_position = current_position
        if current_row:
            self.current_row = current_row
        return self

    def _make_move(self, value, direction=None):
        '''
        Function to update the parameters of the solution tracker based on
        move determined by the solver.

        Parameters
        ----------------------------------
        value : int
            the next value being added to the path
        direction : str
            either 'L' or 'R' indicating the direction to move.

        Returns self
        '''
        self.values.append(value)
        self.current_row += 1
        if not direction:
            return
        if direction == 'L':
            self.output.append(direction)
        elif direction == 'R':
            self.output.append(direction)
            self.current_position += 1
            return self
        else:
            raise ValueError('direction argument must be \'R\' or \'L\'.')
