""" Basic backtracking implementation for solving a sudoku"""

import gui
from file_parser import sudokus


def isvalid(gridstr, x, y, test_value):
    """ Check if it would be legal to place a in pos x,y """
    sq_indexes = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
    group_indexes = [(x_ind, y_ind)
                     for x_ind in sq_indexes[x // 3]
                     for y_ind in sq_indexes[y // 3]]

    for index in range(9):
        # Check squares in the same column
        if gridstr[x + 9 * index] == test_value:
            return False

        # Check the row
        if gridstr[index + 9 * y] == test_value:
            return False

        # Check the group
        x_index, y_index = group_indexes[index]
        if gridstr[x_index + 9 * y_index] == test_value:
            return False

    return True


def solve(gridlst, solutions, x=0, y=0):
    """ Recursive backtracking algorithm """
    if gridlst[x + y * 9] == str(0):
        for test_value in range(1, 10):
            if isvalid(gridlst, x, y, str(test_value)):
                gridlst[x + y * 9] = str(test_value)
                solve(gridlst, solutions, x, y)
            # Backtrack
            gridlst[x + y * 9] = '0'
        # a wasnt 1-9, so this is an invalid grid
        return
    if x == 8:
        if y == 8:
            solutions.append("".join(gridlst))
            return
        solve(gridlst, solutions, 0, y+1)
    else:
        solve(gridlst, solutions, x+1, y)

def main():
    """ Provides questions to solve function and checks answers are correct """
    grid = gui.Grid()
    for qn_no, (puzzle, answer) in enumerate(sudokus()):
        print(f"Now solving grid #{qn_no}")

        # Use update, so only create one instance of grid.
        grid.updategrid(puzzle)
        grid.show_grid()
        gui.eventloop(grid)

        # Solve, providing all solutions
        solutions = []
        solve(list(puzzle), solutions)

        for soln in solutions:
            if answer is not None and soln != answer:
                raise Exception(f"Incorrect solution to qn {qn_no}, {soln}")
            grid.updategrid(soln)
            grid.show_grid()
            gui.eventloop(grid)

if __name__ == '__main__':
    main()
