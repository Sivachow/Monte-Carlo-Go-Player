
from gtp_connection import GtpConnection
from board_util import GoBoardUtil, EMPTY, BLACK, WHITE
from simple_board import SimpleGoBoard
from mcts import MCTS
from pattern_util import PatternUtil


import numpy as np
import random 

def count_at_depth(node, depth, nodesAtDepth):
    if not node._expanded:
        return
    nodesAtDepth[depth] += 1
    for _, child in node._children.items():
        count_at_depth(child, depth + 1, nodesAtDepth)

def undo(board, move):
    board.board[move] = EMPTY
    board.current_player = GoBoardUtil.opponent(board.current_player)

def play_move(board, move, color):
    board.play_move(move, color)

def game_result(board):    
    legal_moves = GoBoardUtil.generate_legal_moves(board, board.current_player)
    if not legal_moves:
        result = BLACK if board.current_player == WHITE else WHITE
    else:
        result = None
    return result

class NoGoFlatMC():
    def __init__(self):
        """
        NoGo player that selects moves by flat Monte Carlo Search.
        Resigns only at the end of game.
        Replace this player's algorithm by your own.

        """
        self.name = "NoGo Assignment 4"
        self.version = 0.0
        self.simulations_per_move = 10
        self.best_move = None
        self.MCTS = MCTS()
        self.num_simulation = 300
        self.limit = 100
        self.exploration = 0.4
        self.simulation_policy = 'random' #simrule must be random or rulebased or prob
        self.use_pattern = True
        self.in_tree_knowledge = "None"
        self.parent = None

    def reset(self):
        self.MCTS = MCTS()

    def update(self, move):
        self.parent = self.MCTS._root
        self.MCTS.update_with_move(move)

    def get_move(self, board, toplay):
        move = self.MCTS.get_move(
            board,
            toplay,
            limit=self.limit,
            use_pattern=self.use_pattern,
            num_simulation=self.num_simulation,
            exploration=self.exploration,
            simulation_policy=self.simulation_policy,
            in_tree_knowledge=self.in_tree_knowledge,
        )
       
        self.update(move)
        return move

    def get_node_depth(self, root):
        MAX_DEPTH = 100
        nodesAtDepth = [0] * MAX_DEPTH
        count_at_depth(root, 0, nodesAtDepth)
        prev_nodes = 1
        return nodesAtDepth

    def get_properties(self):
        return dict(version=self.version, name=self.__class__.__name__,)

def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(NoGoFlatMC(), board)
    con.start_connection()

if __name__=='__main__':
    run()