#!/usr//bin/python3
#/usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection, format_point, point_to_coord
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard
from pattern_util import *
import sys
import ucb

def byPercentage(pair):
    return pair[1]

def writeMoves(board, moves, count, numSimulations):
    """
    Write simulation results for each move.
    """
    gtp_moves = []
    for i in range(len(moves)):
        if moves[i] != None:
            x, y = point_to_coord(moves[i], board.size)
            gtp_moves.append((format_point((x, y)),
                              float(count[i])/float(numSimulations)))
    sys.stderr.write("win rates: {}\n"
                     .format(sorted(gtp_moves, key = byPercentage,
                                    reverse = True)))
sys.stderr.flush()

def select_best_move(board, moves, moveWins):
    """
    Move select after the search.
    """
    max_child = np.argmax(moveWins)
    return moves[max_child]

class Nogo():
    def __init__(self, N, ucb):
        """
        NoGo player that selects moves randomly 
        from the set of legal moves.
        Passe/resigns only at the end of game.

        """
        self.name = "NoGoAssignment4"
        self.version = 3.0
        self.sim = N
        self.use_ucb = ucb
        self.best_move = None
          
    def simulate(self, board, move, toplay):
        """
        Run a simulate game for a given move.
        """
        cboard = board.copy()
        cboard.play_move(move, toplay)
        opp = GoBoardUtil.opponent(toplay)
        return PatternUtil.playGame(cboard,
                                    opp)
    
    def simulateMove(self, board, move, toplay):
        """
        Run simulations for a given move.
        """
        wins = 0
        for _ in range(self.sim):
            result = self.simulate(board, move, toplay)
            if result == toplay:
                wins += 1
        return wins
    
    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        cboard = board.copy()
        moves = GoBoardUtil.generate_legal_moves(board, board.current_player)
        self.best_move = moves[0]
        if not moves:
            return None

        C = 0.4 #sqrt(2) is safe, this is more aggressive
        best = ucb.runUcb(self, cboard, C, moves, color)
        return best
        
        '''
        else:
            moveWins = []
            for move in moves:
                wins = self.simulateMove(cboard, move, color)
                moveWins.append(wins)
            writeMoves(cboard, moves, moveWins, self.sim)
            return select_best_move(board, moves, moveWins)
        '''

def run(sim, selection):
    """
    Start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(Nogo(sim, selection), board)
    con.start_connection()

if __name__=='__main__':
    run(10, False)
