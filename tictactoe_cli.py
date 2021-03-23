import random
from random import randrange

# static game data - doesn't change (hence immutable tuple data type)
WIN_SET = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
    (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
)

# global variables for game data
board = [' '] * 9
current_player = ''  # 'x' or 'o' for first and second player

difficulty = None
gamemode = 0

players = {
    'x': 'Human',
    'o': 'Super AI',  # final comma is optional, but doesn't hurt
}

first_move = True
first_turn = ''
winner = None
move = None

# "horizontal rule", printed as a separator ...
HR = '-' * 40


#==============================================================================
# Game model functions

def check_move():
    '''This function will return True if ``move`` is valid (in the board range
    and free cell), or print an error message and return False if not valid.
    ``move`` is an int board position [0..8].
    '''
    global move
    try:
        move = int(move)
        if board[move] == ' ':
            return True
        else:
            print('>> Sorry - that position is already taken!')
            return False
    except:  # a "bare" except is bad practice, but simple and works still
        print('>> %s is not a valid position! Must be int between 0 and 8.' % move)
        return False


def check_for_result():
    '''Checks the current board to see if there is a winner, tie or not.
    Returns a 'x' or 'o' to indicate a winner, 'tie' for a stale-mate game, or
    simply False if the game is still going.
    '''
    for row in WIN_SET:
        if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
            return board[row[0]]  # return an 'x' or 'o' to indicate winner

    if ' ' not in board:
        return 'tie'

    return None

def block_winning_move():

    block_move = -1

    for row in WIN_SET:

        if board[row[0]] == board[row[1]] == 'x' and board[row[2]] == ' ':
            print('Blocking ' + str(row[2]))
            block_move = row[2]
        elif board[row[0]] == board[row[2]] == 'x' and board[row[1]] == ' ':
            print('Blocking ' + str(row[1]))
            block_move = row[1]
        elif board[row[1]] == board[row[2]] == 'x' and board[row[0]] == ' ':
            print('Blocking ' + str(row[0]))
            block_move = row[0]

    return block_move

def find_my_winning_move():

    ai_move = -1

    for row in WIN_SET:

        if board[row[0]] == board[row[1]] == 'o' and board[row[2]] == ' ':
            ai_move = row[2]
        elif board[row[0]] == board[row[2]] == 'o' and board[row[1]] == ' ':
            ai_move = row[1]
        elif board[row[1]] == board[row[2]] == 'o' and board[row[0]] == ' ':
            ai_move = row[0]

    return ai_move


#==============================================================================
# agent (human or AI) functions


def get_human_move():
    '''Get a human players raw input. Returns None if a number is not entered.'''
    return input('[0-8] >> ')


def get_ai_move():
    '''Get the AI's next move '''
    # A simple dumb random move - valid or NOT!
    # Note: It is the models responsibility to check for valid moves...
    return randrange(9)  # [0..8]

def get_medium_ai_move():
    

    block_move = block_winning_move()

    if block_move != -1:
        return block_move
    else:
        return randrange(9)

def get_hard_ai_move():

	global first_turn, first_move

	corner_move = [0, 2, 6, 8]
	

	while first_move == True:
		if first_turn == 'N' or first_turn == 'n':
			first_move = False
			return 4
		else:
			first_move = False
			return random.choice(corner_move)

	win_move = find_my_winning_move()
	block_move = block_winning_move()

	if win_move != -1:
		return win_move
	elif block_move != -1:
		return block_move
	
	return randrange(9)

#==============================================================================
# Standard trinity of game loop methods (functions)

def process_input():
    '''Get the current players next move.'''
    # save the next move into a global variable
    global move
    if current_player == 'x':
        move = get_human_move()
    elif difficulty == '1':
    	move = get_ai_move()
    elif difficulty == '2':
        move = get_medium_ai_move()
    elif difficulty == '3':
    	move = get_hard_ai_move()


def update_model():
    '''If the current players input is a valid move, update the board and check
    the game model for a winning player. If the game is still going, change the
    current player and continue. If the input was not valid, let the player
    have another go.
    '''
    global winner, current_player

    if check_move():
        # do the new move (which is stored in the global 'move' variable)
        board[move] = current_player
        # check board for winner (now that it's been updated)
        winner = check_for_result()
        # change the current player (regardless of the outcome)
        if current_player == 'x':
            current_player = 'o'
        else:
            current_player = 'x'
    else:
        print('Try again')


def render_board():
    '''Display the current game board to screen.'''

    print('    %s | %s | %s' % tuple(board[:3]))
    print('   -----------')
    print('    %s | %s | %s' % tuple(board[3:6]))
    print('   -----------')
    print('    %s | %s | %s' % tuple(board[6:]))

    # pretty print the current player name
    if winner is None:
        print('The current player is: %s' % players[current_player])


#==============================================================================


def show_human_help():
    '''Show the player help/instructions. '''
    tmp = '''
To make a move enter a number between 0 - 8 and press enter.
The number corresponds to a board position as illustrated:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    '''
    print(tmp)
    print(HR)


#==============================================================================
# Separate the running of the game using a __name__ test. Allows the use of this
# file as an imported module
#==============================================================================


if __name__ == '__main__':
    # Welcome ...
    print('Welcome to the amazing+awesome tic-tac-toe! \n')
    show_human_help()

    #Select bot difficulty 
    print(' \nChoose difficulty:')
    print(' \n1. Easy')
    print(' \n2. Medium')
    print(' \n3. Hard (a.k.a The Win/Tie Machine. You will never win this AI)')

    

    #validate input
    while difficulty != '1' and difficulty != '2' and difficulty != '3' :
        difficulty = input('\nSelect a number [1-3] >> ')
        
        if difficulty != '1' and difficulty != '2' and difficulty != '3' :
            print(gamemode)
            print(' \nPlease type only 1, 2 or 3!')

    # the user selects to go first or second.
    print(' \nDo you want to go first?')
    while first_turn != 'Y' and first_turn != 'y' and first_turn != 'N' and first_turn != 'n':
	    first_turn = input('\n[Y-N] >> ')
	    if first_turn == 'Y' or first_turn == 'y':
	    	current_player = 'x'
	    elif first_turn == 'N' or first_turn == 'n':
	    	current_player = 'o'
	    #validate input
	    else:
	    	print(' \nPlease enter Y or N')

    # show the initial board and the current player's move
    render_board()

    # Standard game loop structure
    while winner is None:
        process_input()
        update_model()
        render_board()

    # Some pretty messages for the result
    print(HR)
    if winner == 'tie':
        print('TIE!')
    elif winner in players:
        print('%s is the WINNER!!!' % players[winner])
    print(HR)
    print('Game over. Press Enter to exit.')
    input('-> ')
