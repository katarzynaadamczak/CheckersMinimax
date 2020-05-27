from Board import *
from Field import Field

MAX_DEPTH = 3
PLAYER1 = "w"
PLAYER2 = "b"


def main():
    board = Board()


def minimax(board, player, depth):
    if is_game_over(board=board) or depth == MAX_DEPTH:
        return board.evaluate()
    children_moves = all_possible_moves_for_player(board, )

    best_score = 0
    if player == PLAYER1:  # max
        best_score = -1000
        for single_move in children_moves:
            score = minimax(single_move, depth + 1)
            if score > best_score:
                best_score = score
    if player == PLAYER2:  # min
        best_score = 1000
        for single_move in children_moves:
            score = minimax(single_move, depth + 1)
            if score < best_score:
                best_score = score
    return best_score


def is_game_over(board):
    if board.count_pawns('w') == 0:
        return True
    if board.count_pawns('b') == 0:
        return True
    return False


# def all_possible_moves_for_player(board, player):
#     moves = []
#     for single_pawn in board.pawns:
#         if single_pawn.color == PLAYER1:
#             if is_pawn_on_field(single_pawn.x+1,single_pawn.y-1) == False:
#                 moves.append(Field())

def get_all_correct_moves(board, player_name, fields, is_capture=False):
    correct_moves = []
    possible_captures = []
    pawns = board.get_player_pawns(player_name)  # get_pieces_for_player_name(board, player_name)
    for pawn in pawns:
        if pawn.pawn == "B" or pawn.pawn == "W":
            correct_moves = get_correct_moves_for_queen(pawn, fields, player_name)
            possible_captures = get_captures_for_queen()
        else:
            correct_moves = get_correct_moves_for_pawn(pawn, fields, player_name, is_capture)
            possible_captures = get_captures_for_pawn()
        correct_moves.append(correct_moves)
        correct_moves.append(possible_captures)
    return correct_moves


def get_correct_moves_for_pawn(board, pawn, player):
    if player == PLAYER1:
        direction = -1
    else:
        direction = 1

    correct_moves = []
    possible_field = Field(pawn.x + 1, pawn.y + direction, pawn.pawn, pawn.value)
    if is_correct_move(board, possible_field):
        new_board = board.copy_board()
        new_board.remove_pawn(pawn)
        new_board.add_pawn(possible_field)
        correct_moves.append(new_board)
    possible_field = Field(pawn.x - 1, pawn.y + direction, pawn.pawn, pawn.value)
    if is_correct_move(board, possible_field):
        new_board = board.copy_board()
        new_board.remove_pawn(pawn)
        new_board.add_pawn(possible_field)
        correct_moves.append(new_board)
    return correct_moves

    # possible_field = Field(pawn.x + 1, pawn.y + direction, pawn.pawn, pawn.value)
    # if is_correct_move(board, possible_field):
    #     correct_moves.append(possible_field)
    # possible_field_to_kill = Field(possible_field.x + 1, possible_field.y + direction, possible_field.pawn, possible_field.value)
    # if is_correct_move(board, possible_field_to_kill):
    #     correct_moves.append(possible_field_to_kill)
    #     next_move = get_correct_moves_for_pawn()
    #
    # # idz na skok o 1 + correct move
    # # idz na skos o 2 i sprzawdz czy zbicie + correct move
    # if is_correct_move(pawn.x + 1, pawn.y + direction, fields, player_name, 1, direction, is_capture):
    #     #
    #     correct_moves.append(Move(x + 1, y, 0, piece.x, piece.y))
    # if is_correct_move(x - 1, y, fields, player_name, -1, direction, is_capture):
    #     correct_moves.append(Move(x - 1, y, 0, piece.x, piece.y))
    # # check for possible capture moves back
    #
    # direction = -direction
    # x = piece.x
    # y = piece.y - 1 * direction
    # if is_correct_move(x + 1, y, fields, player_name, 1, direction, True):
    #     correct_moves.append(Move(x + 1, y, 0, piece.x, piece.y))
    # if is_correct_move(x - 1, y, fields, player_name, -1, direction, True):
    #     correct_moves.append(Move(x - 1, y, 0, piece.x, piece.y))
    # return correct_moves


def get_captures_for_pawn_right(board, pawn, player) -> (Board, None):
    if player == PLAYER1:
        direction = -1
    else:
        direction = 1

    board_with_captured = None
    if board.is_oponent_pawn(player, pawn.x + 1, pawn.y + direction) & board.is_empty_field(pawn.x + 2, pawn.y + (2*direction)):
        future_pawn = Field(pawn.x + 2, pawn.y + (2*direction), pawn.pawn, pawn.value)
        opponent_pawn = Field(pawn.x + 1, pawn.y + direction, "c", 0)
        board_with_captured = board.copy_board()
        board_with_captured.remove_pawn(opponent_pawn)
        board_with_captured.remove_pawn(pawn)
        board_with_captured.add_pawn(future_pawn)
        potential = get_captures_for_pawn_right(board_with_captured, future_pawn, player)
        if potential:
            board_with_captured = potential
    return board_with_captured


def get_captures_for_pawn_left(board, pawn, player) -> (Board, None):
    if player == PLAYER1:
         direction = -1
    else:
        direction = 1

    board_with_captured = None
    if board.is_oponent_pawn(player, pawn.x - 1, pawn.y + direction) & board.is_empty_field(pawn.x - 2, pawn.y + (2*direction)):
        future_pawn = Field(pawn.x - 2, pawn.y + (2*direction), pawn.pawn, pawn.value)
        opponent_pawn = Field(pawn.x - 1, pawn.y + direction, "c", 0)
        board_with_captured = board.copy_board()
        board_with_captured.remove_pawn(opponent_pawn)
        board_with_captured.remove_pawn(pawn)
        board_with_captured.add_pawn(future_pawn)
        potential = get_captures_for_pawn_left(board_with_captured, future_pawn, player)
        if potential:
            board_with_captured = potential
    return board_with_captured

def get_correct_moves_for_queen(board, pawn):
    moves = []
    moves.extend(get_correct_moves_for_queen_directions(board, pawn, 1, 1))
    moves.extend(get_correct_moves_for_queen_directions(board, pawn, -1, 1))
    moves.extend(get_correct_moves_for_queen_directions(board, pawn, -1, -1))
    moves.extend(get_correct_moves_for_queen_directions(board, pawn, 1, -1))
    return moves


def get_correct_moves_for_queen_directions(board, pawn, nx, ny):
    correct_moves = []
    x = pawn.x
    y = pawn.y
    n = 0
    while True:
        x = x + n * nx
        y = y + n * ny
        possible_field = Field(x, y, pawn.pawn, pawn.value)
        if is_correct_move(board, possible_field):
            new_board = board.copy_board()
            new_board.remove_pawn(pawn)
            new_board.add_pawn(possible_field)
            correct_moves.append(new_board)
            n += 1
        else:
            break
    return correct_moves


def get_captures_for_queen():
    while:
        x + n
        y + n
        if friend:
            break
        elif not exists:
            break
        elif oponent:
            if jedno_dalej_wolne:
                ZNALAZLEM
            break
        elif empty:
            idziemy
            dalej, nic
            sie
            nie
            stalo
        raise Exception



def is_correct_move(board, possible_field):
    options = []
    options.append(board.is_empty_field(possible_field))
    options.append(board.does_field_exist(possible_field.x,possible_field.y))
    return all(options)




# def is_possible_to_kill(board, field_start, player):
#     # w dwoch kierunkach kierunkach
#     if player == PLAYER1:
#         direction = -1
#         enemy = PLAYER2
#     else:
#         direction = 1
#         enemy = PLAYER1
#     possible_enemy_right = Field(field_start.x + 1, field_start.y + direction, field_start.pawn, field_start.value)
#     possible_enemy_left = Field(field_start.x - 1, field_start.y - direction, field_start.pawn, field_start.value)
#     possible_field_right = Field(field_start.x + 2, field_start.y + 2 * direction, field_start.pawn, field_start.value)
#     possible_field_left = Field(field_start.x - 2, field_start.y - 2 * direction, field_start.pawn, field_start.value)
#     # sprawdz czy przeciwnik, sprawdz czy za nim puste pole
#     wynik_wielkiego_ifa = False
#     if board.does_field_exist(possible_enemy_right):
#         if board[possible_enemy_right.y][possible_enemy_right.x].pawn == enemy:
#             if board.does_field_exist(possible_field_right):
#                 if board.is_empty_field(possible_field_right):
#                     wynik_wielkiego_ifa = True
#     elif board.does_field_exist(possible_enemy_left):
#         if board[possible_enemy_left.y][possible_enemy_left.x].pawn == enemy:
#             if board.does_field_exist(possible_field_left):
#                 if board.is_empty_field(possible_field_left):
#                     wynik_wielkiego_ifa = True
#     else:
#         wynik_wielkiego_ifa = False
#     return wynik_wielkiego_ifa


main()
