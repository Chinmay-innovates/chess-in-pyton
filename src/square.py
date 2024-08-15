from const import *

class Square:

    ALPHACOLS = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h' }

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    def __str__(self):
        return '(' + str(self.row) + ', ' + str(self.col) + ')'

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # -------------
    # OTHER METHODS
    # -------------

    def has_piece(self):
        return self.piece != None

    def has_ally_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def isEmpty(self):
        return not self.has_piece()

    def isEmpty_or_enemy(self, color):
        return self.isEmpty() or self.has_enemy_piece(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7: return False
        return True
    
    @staticmethod
    def get_alphacol(col):
        alphacols = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h' }
        return alphacols[col]