import pygame
import ui
import player
import board
import numpy as np
from config import BLACK, WHITE

class Othello:
    """
    Game main class.
    """

    def __init__(self):
        """ Show options screen and start game modules"""
        # start
        self.gamma=0.5     #discount factor
        self.learning_rate=0.1
        self.gui = ui.Gui()
        self.board = board.Board()
        self.get_options()

    def get_options(self):
        # set up players
        player1, player2, level = self.gui.show_options()
        if player1 == "human":
            self.now_playing = player.Human(self.gui, BLACK)
        else:
            self.now_playing = player.Computer(self.gui,BLACK)
        if player2 == "human":
            self.other_player = player.Human(self.gui, WHITE)
        else:
            self.other_player = player.Computer(self.gui,WHITE)

        self.gui.show_game()
        self.gui.update(self.board.board, 2, 2, self.now_playing.color)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            if self.board.game_ended():
                whites, blacks, empty = self.board.count_stones()
                if whites > blacks:
                    winner = WHITE
                elif blacks > whites:
                    winner = BLACK
                else:
                    winner = None
                break
            self.now_playing.get_current_board(self.board)
            if self.board.get_valid_moves(self.now_playing.color) != []:
                score,self.board = self.now_playing.get_move()
                whites, blacks, empty = self.board.count_stones()
                self.gui.update(self.board.board, blacks, whites,
                                self.now_playing.color)
            self.now_playing, self.other_player = self.other_player, self.now_playing
        self.gui.show_winner(winner)
        pygame.time.wait(10000)
        self.restart()

    def restart(self):
        self.board = board.Board()
        self.get_options()
        self.run()

def main():
    game = Othello()
    game.run()


if __name__ == '__main__':
    main()

