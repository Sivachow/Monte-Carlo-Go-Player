"""
feature_moves.py
Move generation based on simple features.
"""

#from board_score import winner
from simplejson import load
from board_util import GoBoardUtil, PASS,  BLACK, WHITE
from feature import Features_weight
from feature import Feature
from pattern_util import PatternUtil
import numpy as np
import random

def load_weights():
    weights = {}
    with open('weights.txt') as f:
        lines = f.readlines()
        for line in lines:
            weights[int(line.split()[0])] = float(line.split()[1])
    return weights

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
            if board.is_legal(move, color) and not board.is_eye(move, color):
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

    @staticmethod
    def playGame(board, color, **kwargs): #Refer to NoGo.py PlayGame function in Assignment 3
        """
        Run a simulation game according to give parameters.
        """
        komi = kwargs.pop("komi", 0)
        limit = kwargs.pop("limit", 1000)
        simulation_policy = kwargs.pop("random_simulation", "random")
        simulation_policy = "prob"
        use_pattern = kwargs.pop("use_pattern", True)
        #check_selfatari = kwargs.pop("check_selfatari", True)

        if kwargs:
            raise TypeError("Unexpected **kwargs: %r" % kwargs) 

        if simulation_policy == "random":
            while(True):  #Do we really want a limit?
                color = board.current_player
                move = GoBoardUtil.generate_random_move(board, color)
                if(move == None):
                    break
                board.play_move(move, color)

           
        elif simulation_policy == "prob":
            weights_prob = load_weights()
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
                
                #move = FeatureMoves.generate_move(board)

           
        # elif simulation_policy == "rulebased":
        #     move = PatternUtil.generate_move_with_filter(
        #         board, use_pattern, check_selfatari
        #     )
        
        return BLACK + WHITE - color



