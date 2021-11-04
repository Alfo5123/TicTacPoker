#Define player moves 
import random 

board = [str(i) for i in range(10)]

player1_moves = ['\033[93m•\033[m','\033[93m●\033[m']
player2_moves = ['\033[92m•\033[m','\033[92m●\033[m']

# Sample hands
def sample_random_hands(handsize=7, weights=[0.6, 0.4]):
    player1_hand = random.choices(player1_moves, weights, k=handsize)
    player2_hand = random.choices(player2_moves, weights, k=handsize)
    return(player1_hand, player2_hand)

def fixed_hands(handsize=7, weights=[0.6, 0.4]):
    player1_hand = [player1_moves[0]]*(round(handsize*weights[0])) + [player1_moves[1]]*(round(handsize*weights[1])) 
    player2_hand = [player2_moves[0]]*(round(handsize*weights[0])) + [player2_moves[1]]*(round(handsize*weights[1])) 
    return (player1_hand, player2_hand)

def visualize_hand(hand):
    s =""
    for i,v in enumerate(hand): 
        if i > 0: s += ", "
        s += v 
    print("[" + s + "]")
    ix =""
    for i in range(len(hand)): 
        if i > 0: ix += ", "
        ix += str(i+1)
    print("[" + ix + "]")
                                  

def display_board():
    print(f'''
        | {board[1]} | {board[2]} | {board[3]} |
        -------------
        | {board[4]} | {board[5]} | {board[6]} |
        -------------
        | {board[7]} | {board[8]} | {board[9]} |
        ''')
    
def is_big(piece):
    if piece == player1_moves[1] or piece == player2_moves[1]:
        return True
    return False

def is_first(piece):
    return piece in player1_moves

def is_second(piece):
    return piece in player2_moves

def is_empty(position):
    return (board[position] not in player1_moves) and (board[position] not in player2_moves)

def valid_move(position, hand, piece, verbose=False):
    if len(hand) == 0:
        if verbose: print("=> No pieces left")
        return False
    if position < 1 or position > 9: 
        if verbose: print("=> Invalid position. Try again")
        return False
    if piece < 0 or piece >= len(hand):
        if verbose: print("=> Invalid piece. Try again")
        return False
    if is_big(board[position]):
        if verbose: print("=> Invalid move. Try again")
        return False
    else:
        if is_big(hand[piece]):
            return True
        elif is_empty(position):
            return True
    return False

def make_move(position, hand, piece, string):
    print(position, piece)
    print(string)
    visualize_hand(hand)
    board[position] = hand[piece]
    del hand[piece]
    
def check_winner():
    winning_configs = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    for win in winning_configs:
        if is_first(board[win[0]]) and is_first(board[win[1]]) and is_first(board[win[2]]):
            return 1
        elif is_second(board[win[0]]) and is_second(board[win[1]]) and is_second(board[win[2]]):
            return 2
    return None

def get_computer_move(hand1, hand2):
    ## Heuristics based computer move 
    
    # Check if there is any immediate win, make the move
    for position in range(1,10):
        if not is_big(board[position]) and valid_move(position, hand2, len(hand2)-1): # Last element
            aux = board[position]
            board[position] = hand2[len(hand2)-1]
            if check_winner():
                make_move(position, hand2, len(hand2)-1, 'greedy')
                return
            board[position] = aux
    
    # Check if there is any immediate win for first player
    for position in range(1,10):
        if not is_big(board[position]) and valid_move(position, hand1, len(hand1)-1): 
            aux = board[position]
            board[position] = hand1[len(hand1)-1]
            if check_winner():
                make_move(position, hand2, len(hand2)-1, 'first')
                return
            board[position] = aux
            
    # Check if the center or corners are available first
    center = 5
    if is_empty(center):
        make_move(center, hand2, len(hand2)-1, 'center')
        return

    if not is_big(board[center]) and valid_move(center, hand2, len(hand2)-1):
        make_move(center, hand2, len(hand2)-1, 'center')
        return
    
    corners = [1,3,7,9]
    for corner in corners:
        if is_empty(corner):
            make_move(corner, hand2, 0, 'corner')
            return
        if not is_big(board[corner]) and valid_move(corner, hand2, len(hand2)-1):
            make_move(corner, hand2, len(hand2)-1, 'corner')
            return
    
    # rest of values
    sides = [2,4,6,8]
    for side in sides:
        if is_empty(side):
            make_move(side, hand2, 0, 'rest')
            return
        if not is_big(board[side]) and valid_move(side, hand2, len(hand2)-1):
            make_move(side, hand2, len(hand2)-1, 'rest')
            return
    return

def play():
    h1, h2 = fixed_hands()
    while check_winner() is None and len(h1) > 0:
        display_board()
        print("This is your current hand")
        visualize_hand(h1)
        print('\n# Choose your move position ! [1-9] : ', end='')
        position = int(input())
        print(f'# Choose your piece ! [1-{len(h1)}] : ', end='')
        piece = int(input())-1
        if not valid_move(position, h1, piece, verbose=True):
            print("Not valid. Try another move :)")
            continue
        else:
            make_move(position, h1, piece, '')
            if check_winner():
                display_board()
                print("\nYOU WON!!!")
                return
                
            # COMPUTER RANDOM MOVE
            print("\nComputer..thinking")
            get_computer_move(h1, h2)
            print("Done")
            
            if check_winner():
                display_board()
                print("\nYOU LOST")
                return
                
    print("Draw :D")
        

if __name__ == "__main__":
    play()

