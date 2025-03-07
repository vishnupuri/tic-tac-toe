import random

# Randomize the order that we look at the corners and the sides just to keep 
# things interesting.
corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
random.shuffle(corners)

sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
random.shuffle(sides)


# Function to reset the board to its initial empty state
def reset_board():
    return [
        [" ", " ", " "],  # Row 1
        [" ", " ", " "],  # Row 2
        [" ", " ", " "],  # Row 3
    ]


# Function to check if a move is valid
def is_valid_move(row, col):
    # Check bounds and if the cell is empty (checks if thse values are not
    # present, not in is better since it works on lists, strings data types and
    # not individual types
    return (
        0 <= row < len(board)
        and 0 <= col < len(board[row])
        and board[row][col] == " "
    )  

def find_last_square():
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == " ":
                return [row, col]


# Function to check if there is a winner
def check_winner():
    # Check for horizontal wins
    for row in board:  
        # All cells in the row are the same and not empty
        if ( row[0] == row[1] == row[2] != " "): 
            return True
        
    # Check for vertical wins
    for col in range(3):  
         # All cells in the column are the same and not empty
        if (board[0][col] == board[1][col] == board[2][col] != " "): 
            return True

    # Check left-to-right diagonal    
    if (board[0][0] == board[1][1] == board[2][2] != " "):  
        return True
    
    # Check right-to-left diagonal
    if (board[0][2] == board[1][1] == board[2][0] != " "):  
        # No winning condition met
        return True


# Function to print the board in a visually pleasing format
def print_board():
    # Print row 1
    print(f"{board[0][0]} ╻ {board[0][1]} ╻ {board[0][2]}") 

    # Print horizontal separator
    print("━━╋━━━╋━━")  

     # Print row 2
    print(f"{board[1][0]} ┃ {board[1][1]} ┃ {board[1][2]}") 

    # Print horizontal separator
    print("━━╋━━━╋━━") 

    # Print row 3
    print(f"{board[2][0]} ┃ {board[2][1]} ┃ {board[2][2]}")  


def computer_move():
    # Step 1: Check for a winning move. This looks through all the spots in the
    # board and see if it is valid to make a move. then, it will temporarily 
    # make a move and then it will check if that move is a winning move. 
    # If it isnt, then it undoes the move by replacing it with a space.
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                # Place the winning move
                board[row][col] = "O"
                if check_winner():
                    return  
                
                # Undo move
                board[row][col] = " "  

    # Step 2: Block the opponent's winning move, looks through all the spaces 
    # in the board and if placing X makes it so player 1 wins, it will place
    # O in that position to block it.
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                board[row][col] = "X"
                if check_winner():
                    # Block the move
                    board[row][col] = "O"  
                    return
                
                # Undo move.You do this because the board goes
                # through each position in the board and places a piece 
                # temporarily, and if it doesnt match the condition above,
                # it has to undo it so we do this line of code.
                board[row][col] = " " 

    # Step 3: Look for the specific weakspot
    if move_counter == 3 and (
        (board[0][2] == "X" and board[2][0] == "X")
        or (board[0][0] == "X" and board[2][2] == "X")
    ):
        for row, col in sides:
            if is_valid_move(row, col):
                board[row][col] = "O"
            return

    # Step 4: Try to create a fork
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                board[row][col] = "O"
                if has_fork("O"):
                    return
                board[row][col] = " "

    # Step 5: Block opponent's fork.
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                board[row][col] = "X"
                if has_fork("X"):
                    board[row][col] = "O"
                    return
                 # Undo move
                board[row][col] = " " 

    # Step 6: Now try to prioritize a center spot
    if is_valid_move(1, 1):
        board[1][1] = "O"
        return

    # Step 7: See if we can get a corner spot
    for row, col in corners:
        if is_valid_move(row, col):
            board[row][col] = "O"
            return

    # Step 8: Finally, take a side spot
    for row, col in sides:
        if is_valid_move(row, col):
            board[row][col] = "O"
            return

    raise AssertionError("This line of code should not be reached")


def has_fork(symbol):
    winning_lines(symbol) > 1

# Defines what wins are considered. This predicts what potential wins looks
# like and it is a counter for what wins look like. We can't use check_winner
# since all that does is just check if there is a current winner or not.
def winning_lines(symbol,):
    wins = 0
    for row in board:
        if row[0] == row[1] == row[2] == symbol:
            wins += 1
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == symbol:
            wins += 1
    if board[0][0] == board[1][1] == board[2][2] == symbol:
        wins += 1
    if board[0][2] == board[1][1] == board[2][0] == symbol:
        wins += 1
    return wins


print("Hello, welcome to Tic-Tac-Toe")
board = reset_board()
move_counter = 0
print_board()
print("This is the board. Player 1 is 'X' and Player 2 (Computer) is 'O'.")

# Main game loop
while True:
    if move_counter == 8:
        move = find_last_square()
        row = move[0]
        col = move[1]
    else:
        while True:
            # Player 1's turn
            move = input("Player 1, enter your move (1-9): ").strip()
            if not (move >= "1" and move <= "9" and len(move) == 1):
                print("Invalid input. Try again.")
                continue

            row = (ord(move[0]) - ord("1")) // 3
            col = (ord(move[0]) - ord("1")) % 3

            if not is_valid_move(row, col):
                print("Invalid move. Try again.")
            else:
                break

    board[row][col] = "X"
    print_board()
    if check_winner():
        print("Player 1 wins!")
        break
    if move_counter == 8:
        print("It's a draw")
        break

    move_counter += 1

    # Computer's turn
    print("Computer's Turn!")
    computer_move()
    move_counter += 1
    print_board()
    if check_winner():
        print("Computer wins!")
        break
