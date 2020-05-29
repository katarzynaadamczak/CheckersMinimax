from Board import *
from Field import Field
import time

COUNTERM = 0
COUNTERA = 0
MAX_DEPTH = 3
PLAYER1 = "w"
PLAYER2 = "b"


def main():
    board1 = Board()
    board2 = Board()
    board1.print_board()
    # f1 = Field(2, 1, "b", -10)
    # f2 = Field(3, 2, "b", -10)
    # f3 = Field(1, 4, "w", 10)
    # f4 = Field(2, 3, 'w', 10)
    # board.pawns = [f1, f2, f3, f4]
    # board.fields_with_pawns = board.get_board_with_pawns()

    # # print(board.pawns)
    # board.print_board()
    # print(minimax(board, PLAYER1, 1))
    start1 = time.time()
    run(board1, "mini")
    end1 = time.time()
    start2 = time.time()
    run(board2, "alpha")
    end2 = time.time()
    print("Minimax time: ", (end1 - start1), "Alpha-beta pruning time: ", (end2 - start2))
    print("Minimax nodes: ", COUNTERM, "Alpha-beta pruning nodes: ", COUNTERA)


def run(board, what_algorithm):
    player = PLAYER1
    counter = 0
    while True:
        if counter > 30:
            print("REMIS")
            break
        # print("Before", player, "move:")
        # board.print_board()
        all_pawns_before = board.evaluate()
        if what_algorithm == "mini":
            score, board = minimax(board, player, 0)
        else:
            score, board = alpha_beta(board, player, 0, -10000, 10000)
        all_pawns_after = score
        if all_pawns_after == all_pawns_before:
            counter += 1
        else:
            counter = 0

        player = PLAYER2 if player == PLAYER1 else PLAYER1
        if is_game_over(board):
            break
    board.print_board()


def minimax(board, player, depth):
    global COUNTERM
    COUNTERM += 1

    if is_game_over(board=board) or depth == MAX_DEPTH:
        return board.evaluate(), board
    children_moves = get_all_correct_moves(board, player)

    best_score = 0
    best_board = board
    if player == PLAYER1:  # max
        best_score = -10000
        for single_board in children_moves:
            temp_board = single_board
            score, potential_board = minimax(single_board, player=PLAYER2, depth=depth + 1)
            if score > best_score:
                best_score = score
                best_board = temp_board
    if player == PLAYER2:  # min
        best_score = 10000
        for single_board in children_moves:
            temp_board = single_board
            score, potential_board = minimax(single_board, player=PLAYER1, depth=depth + 1)
            if score < best_score:
                best_score = score
                best_board = temp_board
    return best_score, best_board


def alpha_beta(board, player, depth, alpha, beta):
    global COUNTERA
    COUNTERA += 1

    if is_game_over(board=board) or depth == MAX_DEPTH:
        return board.evaluate(), board
    children_moves = get_all_correct_moves(board, player)

    best_score = 0
    best_board = board
    if player == PLAYER1:  # max
        best_score = -10000
        for single_board in children_moves:
            score, potential_board = alpha_beta(single_board, player=PLAYER2, depth=depth + 1, alpha=alpha, beta=beta)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            best_board = potential_board
            if alpha >= beta:
                break
        return best_score, best_board
    if player == PLAYER2:  # min
        best_score = 10000
        for single_board in children_moves:
            score, potential_board = alpha_beta(single_board, player=PLAYER1, depth=depth + 1, alpha=alpha, beta=beta)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            best_board = potential_board
            if beta <= alpha:
                break
        return best_score, best_board


def is_game_over(board):
    if board.count_pawns('w') == 0:
        return True
    if board.count_pawns('b') == 0:
        return True
    return False


def get_all_correct_moves(board, player):
    correct_moves = []
    possible_captures = []
    pawns = board.get_player_pawns(player)  # get_pieces_for_player_name(board, player_name)
    # print("start")
    for pawn in pawns:
        if pawn.pawn.isupper():
            correct_moves.extend(get_correct_moves_for_queen(board, pawn))
            possible_captures = get_captures_for_queen(board, pawn, player)
            correct_moves.extend(possible_captures) if possible_captures else None
            # print(correct_moves)
        else:
            correct_moves.extend(get_correct_moves_for_pawn(board, pawn, player))
            possible_captures_right = get_captures_for_pawn_right(board, pawn, player)

            correct_moves.append(possible_captures_right) if possible_captures_right else None
            possible_captures_left = get_captures_for_pawn_left(board, pawn, player)

            correct_moves.append(possible_captures_left) if possible_captures_left else None

    return correct_moves


def get_correct_moves_for_pawn(board, pawn, player):
    if player == PLAYER1:
        direction = 1
    else:
        direction = -1

    correct_moves = []
    possible_field = Field(pawn.x + 1, pawn.y + direction, pawn.pawn, pawn.value)
    if is_correct_move(board, possible_field):
        new_board = board.copy_board()
        new_board.remove_pawn(pawn)
        if board.is_on_edge(possible_field.x, possible_field.y):
            possible_field = board.pawn_to_queen(possible_field)
        new_board.add_pawn(possible_field)
        correct_moves.append(new_board)
    possible_field = Field(pawn.x - 1, pawn.y + direction, pawn.pawn, pawn.value)
    if is_correct_move(board, possible_field):
        new_board = board.copy_board()
        new_board.remove_pawn(pawn)
        if board.is_on_edge(possible_field.x, possible_field.y):
            possible_field = board.pawn_to_queen(possible_field)
        new_board.add_pawn(possible_field)
        correct_moves.append(new_board)
    return correct_moves


def get_captures_for_pawn_right(board, pawn, player) -> (Board, None):
    if player == PLAYER1:
        direction = 1
    else:
        direction = -1

    board_with_captured = None
    if board.does_field_exist(pawn.x + 1, pawn.y + direction) and board.does_field_exist(pawn.x + 2,
                                                                                         pawn.y + (2 * direction)):
        if board.is_opponent_pawn(player, pawn.x + 1, pawn.y + direction) and board.is_empty_field(pawn.x + 2,
                                                                                                   pawn.y + (
                                                                                                           2 * direction)):
            future_pawn = Field(pawn.x + 2, pawn.y + (2 * direction), pawn.pawn, pawn.value)
            opponent_pawn = Field(pawn.x + 1, pawn.y + direction, "c", 0)
            board_with_captured = board.copy_board()
            board_with_captured.remove_pawn(opponent_pawn)
            board_with_captured.remove_pawn(pawn)
            if board.is_on_edge(future_pawn.x, future_pawn.y):
                future_pawn = board.pawn_to_queen(future_pawn)
            board_with_captured.add_pawn(future_pawn)
            potential = get_captures_for_pawn_right(board_with_captured, future_pawn, player)
            if potential:
                board_with_captured = potential
    return board_with_captured


def get_captures_for_pawn_left(board, pawn, player) -> (Board, None):
    if player == PLAYER1:
        direction = 1
    else:
        direction = -1

    board_with_captured = None
    if board.does_field_exist(pawn.x - 1, pawn.y + direction) and board.does_field_exist(pawn.x - 2,
                                                                                         pawn.y + (2 * direction)):
        if board.is_opponent_pawn(player, pawn.x - 1, pawn.y + direction) and board.is_empty_field(pawn.x - 2,
                                                                                                   pawn.y + (
                                                                                                           2 * direction)):
            future_pawn = Field(pawn.x - 2, pawn.y + (2 * direction), pawn.pawn, pawn.value)
            opponent_pawn = Field(pawn.x - 1, pawn.y + direction, "c", 0)
            board_with_captured = board.copy_board()
            board_with_captured.remove_pawn(opponent_pawn)
            board_with_captured.remove_pawn(pawn)
            if board.is_on_edge(future_pawn.x, future_pawn.y):
                future_pawn = board.pawn_to_queen(future_pawn)
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
    # print(moves)
    return moves


def get_correct_moves_for_queen_directions(board, pawn, nx, ny):
    correct_moves = []
    x = pawn.x
    y = pawn.y
    n = 1
    while True:
        x = x + n * nx
        y = y + n * ny
        possible_field = Field(x, y, pawn.pawn, pawn.value)
        if is_correct_move(board, possible_field):
            new_board = board.copy_board()
            new_board.remove_pawn(pawn)
            new_board.add_pawn(possible_field)
            correct_moves.append(new_board)

        else:
            break
        n += 1
    # print(correct_moves)
    return correct_moves


def get_captures_for_queen(board, pawn, player) -> list:
    moves = []
    moves.extend(get_captures_for_queen_directions(board, pawn, player, 1, 1))
    moves.extend(get_captures_for_queen_directions(board, pawn, player, -1, 1))
    moves.extend(get_captures_for_queen_directions(board, pawn, player, -1, -1))
    moves.extend(get_captures_for_queen_directions(board, pawn, player, 1, -1))
    # print(moves)
    return moves


def get_captures_for_queen_directions(board, pawn, player, nx, ny):
    x = pawn.x
    y = pawn.y
    n = 0
    board_with_captured = []
    while True:
        x = x + n * nx
        y = y + n * ny
        if board.does_field_exist(x, y):
            if board.is_opponent_pawn(player, x, y):
                if is_correct_move(board, Field(x + nx, y + ny, "c", 100)):
                    # print("oponen")
                    future_pawn = Field(x + nx, y + ny, pawn.pawn, pawn.value)
                    opponent_pawn = Field(x, y, "c", 0)
                    new_board = board.copy_board()
                    new_board.remove_pawn(pawn)
                    new_board.remove_pawn(opponent_pawn)
                    new_board.add_pawn(future_pawn)
                    board_with_captured = [new_board]

                    break
        else:
            break
        n += 1
    return board_with_captured


def is_correct_move(board, possible_field):
    if board.does_field_exist(possible_field.x, possible_field.y):
        if board.is_empty_field(possible_field.x, possible_field.y):
            return True
    return False


main()
