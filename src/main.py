import sys, pygame

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()


    def mainloop(self):
        game=self.game
        screen=self.screen
        dragger =self.game.dragger
        board= self.game.board

        # game loop starts here
        while True:
            #show methord
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                # clicked sqaure has a piece?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece =  board.squares[clicked_row][clicked_col].piece
                        #valid piece (color) ?
                        if piece.color==game.next_player:
                            board.calc_moves(piece,clicked_row,clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            #show methord
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methord
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)
                # mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                   
                   if dragger.dragging:
                       dragger.update_mouse(event.pos)

                       released_row = dragger.mouseY // SQSIZE
                       released_col = dragger.mouseX // SQSIZE

                       #create possible move
                       initial = Square(dragger.initial_row,dragger.initial_col) 
                       final = Square(released_row, released_col)
                       move = Move(initial, final)
                       
                       # valid move ?
                       if board.valid_move(dragger.piece,move):
                           board.move(dragger.piece,move)
                           # show methord
                           game.show_bg(screen)
                           game.show_last_move(screen)
                           game.show_pieces(screen)
                           # next turn
                           game.next_turn()

                   dragger.undrag_piece()
                # quit the app
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()