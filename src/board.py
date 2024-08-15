from const import *
from move import Move
from square import Square
from piece import *
class Board:
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for _col in range(COLS)]
        self.last_move=None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self,piece,move):
        '''
            Move a piece to a specific position
        '''
        initial = move.initial
        final = move.final
        # console board move update
        self.squares[initial.row][initial.col].piece=None
        self.squares[final.row][final.col].piece=piece

        # move
        piece.moved = True

        # clear valid moves 
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self,piece,move):
        return move in piece.moves 

    def calc_moves(self,piece,row,col):
         '''
            Calculate  all the posible (valid) moves of a specific piece on a specific position 
         '''
         def knight_moves():
             # 8 possible moves
             possible_moves =[
                 (row-2,col+1), # front right
                 (row-1,col+2), # left front
                 (row+1,col+2), # left back
                 (row+2,col+1), # back right
                 (row+2,col-1), # back left
                 (row+1,col-2), # right back
                 (row-1,col-2), # right front
                 (row-2,col-1), # front left
            ]
             for possible_move in possible_moves:
                 possible_move_row,possible_move_col = possible_move
                 if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isEmpty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row,col)
                        final = Square(possible_move_row,possible_move_col)
                        # create  new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
                          
         def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            #vertical moves 
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end , piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isEmpty():
                        # create initial , final squares of the move
                        initial = Square(row,col)
                        final = Square(possible_move_row,col)
                        # create  new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
                    # blocked 
                    else : break
                # not iin range
                else : break 

            #diagonal moves 
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1 , col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial , final squares of the move
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col)
                        # create  new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
                        
         def straight_line_moves(increaments):
             for increament in increaments:
                row_inc, col_inc = increament
                possible_move_row = row + row_inc
                possible_move_col = col + col_inc
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col, self.squares[possible_move_row][possible_move_col].piece)
                        move = Move(initial, final)
                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isEmpty():
                            # append new move
                            piece.add_move(move)
                        # piece 
                        else: 
                            if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                                # new move and stop
                                piece.add_move(move)
                            break
                    else: # not in range
                        break
                    # increment move
                    possible_move_row, possible_move_col = possible_move_row + row_inc, possible_move_col + col_inc

         def king_moves():
            adjacent_squares = [
                (row - 1, col + 0),#up
                (row - 1, col + 1),#up-right
                (row + 0, col + 1),#right
                (row + 1, col + 1),#down-right
                (row + 1, col + 0),#down
                (row + 1, col - 1),#down-left
                (row + 0, col - 1),#left
                (row - 1, col - 1),#up-left
            ]
            # normal moves
            for adjacent in adjacent_squares:
                move_row, move_col = adjacent
                
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isEmpty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
            
            #castling

            #queen-side castling
            
            #king-side castling

         if isinstance(piece,Pawn):
            pawn_moves()
         elif isinstance(piece, Knight):
            knight_moves()
         elif isinstance(piece, Bishop):
            straight_line_moves([
                (-1 , 1), # upper right 
                (-1 , -1), # upper left
                (1 , -1), # bottom left
                (1 , 1) # bottom right
            ])
         elif isinstance(piece, Rook):
            straight_line_moves([
                (-1 , 0), # up
                (0 , 1), # right
                (1 , 0), # down
                (0 , -1) # left
            ])
         elif isinstance(piece, Queen):
            straight_line_moves([
                (-1 , 1), # upper right 
                (-1 , -1), # upper left
                (1 , -1), # bottom left
                (1 , 1), # bottom right
                (-1 , 0), # up
                (0 , 1), # right
                (1 , 0), # down
                (0 , -1) # left
            ])
         elif isinstance(piece, King):
            king_moves()

    # _create , _add_piece are private methods
    def _create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                    self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))