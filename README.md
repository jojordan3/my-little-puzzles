# Collection of fun little puzzles

## TrianglePuzzle
The triangle puzzle is set up as a triangle of numbers with the point of the triangle facing up. The objective of this puzzle is to find the path from the number at the top of the triangle all down to the bottom row such that the product of all the values visited is equal to a specified target number.

The first row of the triangle is a single, positive integer, the second row contains two positive integers, and so on, creating the triangle. Starting from the initial position at the top of the triangle, the player continually moves down one row at a time by moving to the value down and to the left ('L') of the current position, or down and to the right ('R') of the current position--until the player reaches the bottom row. In this way, the player visits the same number of values as there are rows in the triangle. The player must find the path that makes the product of all the values visited equal to the specified target value. The solution is the moves the player took to get to the bottom.

### Example
Say we had this triangle:

          3
      5       3
  2       5       6

With a target of 45.

The solution would be 'RL', so that we would visit 3, 3, and 5 (3*3*5=45).

The TrianglePuzzle class can read puzzles from a .txt file, generate random puzzles, ensure puzzles are valid triangle puzzles, and solve puzzles.
