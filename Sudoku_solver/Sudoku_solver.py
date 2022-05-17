def is_right(matrix, row, col, value):
    '''
    Check if it is right to insert a 'value' into a matrix at position (row, col)
    input:
        matrix: numpy array, the Sudoku matrix
        row: int, the row where we will insert the value
        col: int, the column where we will insert the value
        value: int, the value that we insert into the matrix at position (row, col)
    return:
        True if is is right to insert the value into the matrix
        False if not
    '''

    # Check if the value is duplicated in a row
    if value in matrix[row]:
        return False

    # Check if the value is duplicated in a column
    if value in matrix[:, col]:
        return False

    # Check if the value is duplicated in a grid 3x3
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if matrix[i + startRow][j + startCol] == value:
                return False

    return True

def solve_Sudoku(matrix, row, col):
    '''
    The function that uses back-tracking algorithm to solve the Sudoku
    input:
        matrix: numpy array, the Sudoku matrix
        row: int, the row where we will insert the value
        col: int, the column where we will insert the value
    return
        matrix: the matrix of Sudoku which is solved
        state: if the Sudoku is solved or not

    '''

    # Check if the cursor (position of value that we will insert) is at the end of matrix
    if row==8 and col==9:
        return (matrix, True)

    # if the cursor reaches the end of a row -> move to next row
    if col == 9:
        row += 1
        col = 0

    # Check if the current position of the matrix already contains value > 0, we move to next column
    if matrix[row][col] > 0:
        return solve_Sudoku(matrix, row, col + 1)

    # iterate from 1 to 9 to check which number is correct to insert into the position
    for i in range(1, 10):
        # Check if i is right to insert into the position
        if is_right(matrix, row, col, i):
            matrix[row][col] = i
            if solve_Sudoku(matrix, row, col+1)[1]:
                return (matrix, True)

        # if the number is wrong, assign it back to 0
        matrix[row][col] = 0

    # if the Sudoku cannot be solved
    return (matrix, False)