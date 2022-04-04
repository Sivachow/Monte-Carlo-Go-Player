"""
feature_moves.py
Move generation based on simple features.
"""

from board_util import GoBoardUtil
from feature import Features_weight
from feature import Feature
import numpy as np
import random

class FeatureMoves(object):
    @staticmethod
    def generate_moves(board):

        assert len(Features_weight) != 0
        moves = []
        gamma_sum = 0.0
        empty_points = board.get_empty_points()
        color = board.current_player
        probs = np.zeros(board.maxpoint)
        all_board_features = Feature.find_all_features(board)
        for move in empty_points:
            if board.is_legal(move, color):
                moves.append(move)
                probs[move] = Feature.compute_move_gamma(
                    Features_weight, all_board_features[move]
                )
                gamma_sum += probs[move]
        if len(moves) != 0:
            assert gamma_sum != 0.0
            for m in moves:
                probs[m] = probs[m] / gamma_sum
        return moves, probs

    @staticmethod
    def generate_move(board):
        moves, probs = FeatureMoves.generate_moves(board)
        if len(moves) == 0:
            return None
        return np.random.choice(board.maxpoint, 1, p=probs)[0]

    @staticmethod
    def generate_move_with_feature_based_probs_max(board):
        """Used for UI"""
        moves, probs = FeatureMoves.generate_moves(board)
        move_prob_tuple = []
        for m in moves:
            move_prob_tuple.append((m, probs[m]))
        return sorted(move_prob_tuple, key=lambda i: i[1], reverse=True)[0][0]

    