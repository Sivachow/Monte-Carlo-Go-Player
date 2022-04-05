"""
pattern_util.py
Utility functions for rule based simulations.
"""

import numpy as np
#from pattern import pat3set
import random

from board_util import GoBoardUtil, EMPTY, PASS, BORDER

def get_pattern(board, point, color):
    neighbors = sorted(board._neighbors(point)+board._diag_neighbors(point))
    pattern = ''
    for nb in neighbors:
        # print(nb, format_point(point_to_coord(nb, self.board.size)), board.board[nb])
        pattern += str(board.board[nb])
    return pattern

def get_pattern_probs(board, moves, color, weights):
    
    pattern_moves = {}
    weight_sum = 0
    for move in moves:
        #play move
        board.play_move(move, color)

        pattern = get_pattern(board, move, color)
        address = int(pattern,4)
        #point = format_point(point_to_coord(move, board.size)).lower()
        pattern_moves[move] = weights[address]
        weight_sum += weights[address]

        #undo move
        board.board[move] = 0
        board.current_player = color

    return pattern_moves, weight_sum

class PatternUtil(object):



    @staticmethod
    def playGame(board, color, weights_prob, **kwargs):
        """
        Run a simulation game according to give parameters.
        """
        simulation_policy = kwargs.pop('random_simulation','rulebased')
        use_pattern = kwargs.pop('use_pattern',True)
        #check_selfatari = kwargs.pop('check_selfatari',True)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        simulation_policy = 'prob'
        if simulation_policy == "random":
            while(True):  
                color = board.current_player
                move = GoBoardUtil.generate_random_move(board, color)
                if(move == None):
                    break
                board.play_move(move, color)

        elif simulation_policy == "prob":
            while(True):
                color = board.current_player
                legal_moves = GoBoardUtil.generate_legal_moves(board, color)
                if not legal_moves:
                    break
                pattern_moves = get_pattern_probs(board, legal_moves, color,weights_prob)[0] #Get a dictionary of all the legal moves with their weights
                moves = list(pattern_moves.keys())
                weights = list(pattern_moves.values())
                
                move = random.choices(moves, weights = weights, k=1)[0] #Generate a random move from moves based on weights
                #print(move)
                board.play_move(move, color)


        winner = GoBoardUtil.opponent(color)
        return winner
