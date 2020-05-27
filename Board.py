from Field import Field


class Board:
    def __init__(self):
        self.fields = self.make_fields()
        self.pawns = self.create_pawns()
        self.fields_with_pawns = self.get_board_with_pawns()

    @staticmethod
    def make_fields():
        fields = []
        for i in range(8):
            row = []
            for j in range(8):
                if (i + j) % 2 == 1:
                    row.append(Field(j, i, "_", 0))
                else:
                    row.append(Field(j, i, "  ", 0))
            fields.append(row)
        return fields

    @staticmethod
    def create_pawns():
        pawns = []
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    pawns.append(Field(j, i, "w", 1))
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    pawns.append(Field(j, i, "b", -1))
        return pawns

    def count_pawns(self, color):
        suma = 0
        for single_field_with_pawn in self.pawns:
            if single_field_with_pawn.pawn.lower() == color.lower():
                suma += single_field_with_pawn.value
        return suma

    def evaluate(self):
        suma = 0
        for pawn in self.pawns:
            suma += pawn.value
        return suma

    def get_player_pawns(self, player):
        all_pawns = []
        if player == "b":
            for pawn in self.pawns:
                if pawn.pawn == "b":
                    all_pawns.append(pawn)
        if player == "w":
            for pawn in self.pawns:
                if pawn.pawn == "w":
                    all_pawns.append(pawn)
        return all_pawns

    def get_board_with_pawns(self):
        board_with_pawn = self.make_fields()
        for pawn in self.pawns:
            board_with_pawn[pawn.y][pawn.x].pawn = pawn.pawn
        return board_with_pawn

    def print_board(self):
        board_with_pawn = self.get_board_with_pawns()
        for row in board_with_pawn:
            for field in row:
                print(field.pawn, end="")
            print()

    def is_empty_field(self, x, y):
        board = self.get_board_with_pawns()
        return bool(board[y][x].value)

    def does_field_exist(self, x, y):
        board = self.get_board_with_pawns()
        try:
            get_field = isinstance(board[y][x], Field)
        except Exception:
            return False
        return get_field

    def copy_board(self):
        new_board = Board()
        new_board.fields = self.fields
        new_board.pawns = self.pawns
        new_board.fields_with_pawns = self.fields_with_pawns
        return new_board

    def remove_pawn(self, pawn: Field):
        for i, each in enumerate(self.pawns):
            if each.x == pawn.x & each.y == pawn.y:
                self.pawns.pop(i)
                self.fields_with_pawns = self.get_board_with_pawns()
                return 0
        raise Exception("Could not find pawn in board")

    def add_pawn(self, pawn: Field):
        self.pawns.append(pawn)
        self.fields_with_pawns = self.get_board_with_pawns()

    def is_opponent_pawn(self, player, x, y):
        if not self.is_empty_field(x, y):
            if self.pawns[y][x].pawn.lower() != player:
                return True
        return False


w = Board()
w.print_board()
