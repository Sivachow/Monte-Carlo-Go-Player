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
        komi = kwargs.pop('komi', 0)
        limit = kwargs.pop('limit', 1000)
        simulation_policy = kwargs.pop('random_simulation','rulebased')
        use_pattern = kwargs.pop('use_pattern',True)
        #check_selfatari = kwargs.pop('check_selfatari',True)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        nuPasses = 0
        # simulation_policy = 'prob'
        for _ in range(limit):
            color = board.current_player
            if simulation_policy == 'random':
                move = GoBoardUtil.generate_random_move(board,color,True)
            
            else:
                assert simulation_policy == 'prob'
                legal_moves = GoBoardUtil.generate_legal_moves(board, color)
                if not legal_moves:
                    break
                pattern_moves = get_pattern_probs(board, legal_moves, color,weights_prob)[0] #Get a dictionary of all the legal moves with their weights
                moves = list(pattern_moves.keys())
                weights = list(pattern_moves.values())
                
                move = random.choices(moves, weights = weights, k=1)[0] #Generate a random move from moves based on weights
            if move == PASS:
                break
            board.play_move(move, color)
        winner = GoBoardUtil.opponent(color)
        return winner

    @staticmethod
    def generate_moves_with_feature_based_probs(board):
        from feature import Features_weight
        from feature import Feature
        assert len(Features_weight) != 0
        moves = []
        gamma_sum = 0.0
        empty_points = board.get_empty_points()
        color = board.current_player
        probs = np.zeros(board.maxpoint)
        all_board_features = Feature.find_all_features(board)
        for move in empty_points:
            if board.is_legal(move, color): #and not board.is_eye(move, color):
                moves.append(move)
                probs[move] = Feature.compute_move_gamma(Features_weight, all_board_features[move])
                gamma_sum += probs[move]
        if len(moves) != 0:
            assert gamma_sum != 0.0
            for m in moves:
                probs[m] = probs[m] / gamma_sum
        return moves, probs
    
    @staticmethod
    def generate_move_with_feature_based_probs(board):
        moves, probs = PatternUtil.generate_moves_with_feature_based_probs(board)
        if len(moves) == 0:
            return None
        return np.random.choice(board.maxpoint, 1, p=probs)[0]
    
    @staticmethod
    def generate_move_with_feature_based_probs_max(board):
        """Used for UI"""
        moves, probs = PatternUtil.generate_moves_with_feature_based_probs(board)
        move_prob_tuple = []
        for m in moves:
            move_prob_tuple.append((m, probs[m]))
        return sorted(move_prob_tuple,key=lambda i:i[1],reverse=True)[0][0]
