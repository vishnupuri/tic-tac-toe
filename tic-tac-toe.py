import random

# Randomize the order that we look at the corners and the sides just to keep
# things interestings.
corners = [(0, 0), (0, 2), (2, 0), (2, 2)] 
random.shuffle(corners)

sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
random.shuffle(sides)

# Function to reset the board to its initial empty state
def reset_board():
   return [
       [" ", " ", " "],  # Row 1
       [" ", " ", " "],  # Row 2
       [" ", " ", " "]   # Row 3
]

board = reset_board()
# Function to check if a move is valid
def is_valid_move(row, col):
   return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " "  # Check bounds and if the cell is emptyl (checks if thse values are not present, not in is better since it works on lists, strings data types and not individual types)


# Function to check if there is a winner
def check_winner():
   for row in board:  # Check for horizontal wins
       if row[0] == row[1] == row[2] != ' ':  # All cells in the row are the same and not empty
           return row
   for col in range(3):  # Check for vertical wins
       if board[0][col] == board[1][col] == board[2][col] != ' ':  # All cells in the column are the same and not empty
           return True
   if board[0][0] == board[1][1] == board[2][2] != " ":  # Check left-to-right diagonal
       return True
   if board[0][2] == board[1][1] == board[2][0] != ' ':  # Check right-to-left diagonal
       return True
   return False  # No winning condition met


# Function to print the board in a visually pleasing format
def print_board2():
   print(f"{board[0][0]} ╻ {board[0][1]} ╻ {board[0][2]}")  # Print row 1
   print("━━╋━━━╋━━")  # Print horizontal separator
   print(f"{board[1][0]} ┃ {board[1][1]} ┃ {board[1][2]}")  # Print row 2
   print("━━╋━━━╋━━")  # Print horizontal separator
   print(f"{board[2][0]} ┃ {board[2][1]} ┃ {board[2][2]}")  # Print row 3


def computer_move():
    # Step 1: Check for a winning move. This looks through all the spots in the board and see if it is valid to make a move. then, it will temporarily make a move and then it will check if that move is a winning move. if it isnt, then it undoes the move by replacing it with a space.
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                board[row][col] = 'O'
                if check_winner():
                    return  # Place the winning move
                board[row][col] = ' '  # Undo move

    # Step 2: Block the opponent's winning move, looks through all the spaces in the board and if placing X makes it so player 1 wins, it will place O in that position to block it.
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                board[row][col] = 'X'
                if check_winner():
                    board[row][col] = 'O'  # Block the move
                    return
                board[row][col] = ' '  # Undo move. you do this because the board goes through each position in the board and places a piece temporarily, and if it doesnt match the condition above, it has to undo it so we do this line of code.

    # Step 3: Try to create a fork
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                board[row][col] = 'O'
                forks = count_forks('O')
                if forks >= 2:  # If the move creates a fork
                    return
                board[row][col] = ' '  # Undo move

    # Step 4: Block opponent's fork
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                board[row][col] = 'X'
                forks = count_forks('X')
                if forks >= 2: # If the move blocks a fork
                    board[row][col] = 'O'
                    return
                board[row][col] = ' '  # Undo move

    # Step 5: See if we can get the center spot
    if is_valid_move(1, 1):
        board[1][1] = 'O'
        return

    # Step 6: Now try to get a corner
    for row, col in corners:
        if is_valid_move(row, col):
            board[row][col] = 'O'
            return

    # Step 7: Finally, take a side spot
    for row, col in sides:
        if is_valid_move(row, col):
            board[row][col] = 'O'
            return
            
    raise AssertionError("This line of code should not be reached")
    

def count_forks(symbol):
    fork_count = 0
    for row in range(3):
        for col in range(3):
            if is_valid_move(row, col):
                board[row][col] = symbol
                if winning_lines(symbol) > 1:
                    fork_count += 1 # total the number of possible moves that creates a fork
                board[row][col] = ' '
    return fork_count

def winning_lines(symbol): #defines what wins are considered. This predicts what potential wins look like and it is a counter for what wins look like. We cant use check_winner since all that does is just check if there is a current winner or not.
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

    
# Main game loop
while True:
    print('Hello, welcome to Tic-Tac-Toe')
    play = input('Would you like to play? (yes/no): ').strip().lower()
    if play == 'yes':
        board = reset_board()
        move_counter = 0
        print_board2()
        print("This is the board. Player 1 is 'X' and Player 2 (Computer) is 'O'.")
        
        while True:
            # Player 1's turn
            move = input("Player 1, enter your move (1-9): ").strip()
            if not (move >= "1" and move <= "9" and len(move) == 1):
                print("Invalid input. Try again.")
                continue

            row = (ord(move[0]) - ord('1')) // 3
            col = (ord(move[0]) - ord('1')) % 3

            if is_valid_move(row, col):
                board[row][col] = 'X'
                move_counter += 1
                print_board2()
                if check_winner():
                    print("Player 1 wins!")
                    break
                if move_counter == 9:  
                    print("It's a draw!")
                    break
            else:
                print("Invalid move. Try again.")
                continue
            
            # Computer's turn
            
            print("Computer's Turn!")
            computer_move()
            move_counter += 1
            print_board2()
            if check_winner():
                print("Computer wins!")
                break
        
        play_again = input("Would you like to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break
    elif play == 'no':
        print("Thanks for playing!")
        break
    else:
        print("Invalid choice! Please enter 'yes' or 'no'.")