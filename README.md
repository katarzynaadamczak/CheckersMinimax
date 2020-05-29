# CheckersMinimax
Checkers game using Minimax algorithm and alpha-beta prunning
Checkers implementation rules:
  • Evaluation function:
    o Each pawn has value of 1 (white) or -1 (black)
    o Each queen has value of 10 (white) or -10 (black)
    o Evaluation function = sum of whites values + sum of blacks values
  • Rules:
    o Pawn can go left or right in only one way
    o Blacks go up, whites go down
    o Queen can go in every direction
    o Player’s pawn can capture opponent’s pawn/queen in only one direction (up for blacks, down for whites) and there can be multiple      captures
    o Player’s queen can capture opponent’s pawn/queen in every direction
    o If player’s pawn goes to the opponent’s edge it becomes queen
  • Game ends if there is only one colour of pawns on board or there are no captures after 30 moves
