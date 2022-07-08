def find_empty_grid(x):
    """
    Checks for empty spaces on the puzzle (0's)
    """
    for i in range(len(x)):
        for j in range(len(x[0])):
            if x[i][j] == 0:
                return (i, j) # return row, col

    return None

def solve_array(x):
    """
    Solve the puzzle
    """
    find = find_empty_grid(x) # find the empty spaces
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(x, i, (row, col)): # check constraints
            x[row][col] = i

            if solve_array(x):
                return True

            x[row][col] = 0

    return False

def valid(x, num, pos):
    """
    Function to check location restraints
    """
    # check row
    for i in range(len(x[0])):
        if x[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(x)):
        if x[i][pos[1]] == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if x[i][j] == num and (i, j) != pos:
                return False

    return True

def print_board(x):
    """
    Function to nicely output puzzle board to terminal
    """
    for i in range(len(x)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(x[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                k = "." if x[i][j] == 0 else str(x[i][j])
                print(k)
            else:
                k = "." if x[i][j] == 0 else str(x[i][j])
                print(k + " ", end="")