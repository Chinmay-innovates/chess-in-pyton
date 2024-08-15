import pygame

from const import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger =Dragger()
    #show methords
    def show_bg(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                # color of square (light green and dark green)
                color = (235,236,208)  if(row + col) % 2 == 0 else (119,149,86)
                rect = (col*SQSIZE ,row*SQSIZE ,SQSIZE,SQSIZE)
                pygame.draw.rect(surface, color, rect)
    
    def show_pieces(self,surface):
         for row in range(ROWS):
            for col in range(COLS):
                # is there a piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # all pieces execpt  dragging piece
                    if piece is not self.dragger.piece:
                       piece.set_texture(size=80)
                       img =pygame.image.load(piece.texture)
                       img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                       piece.texture_rect=img.get_rect(center=img_center)
                       surface.blit(img, piece.texture_rect)

    def show_moves(self,surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            # loop all valid moves
            for move in piece.moves:
                #color
                color ='#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                #rect
                rect = (move.final.col*SQSIZE,move.final.row*SQSIZE,SQSIZE,SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)

    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
