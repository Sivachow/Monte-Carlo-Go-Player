"""
pattern_util.py
Utility functions for rule based simulations.
"""

import numpy as np
#from pattern import pat3set
import random

from board_util import GoBoardUtil, EMPTY, PASS, BORDER


class PatternUtil(object):

    @staticmethod
    def playGame(board, color, **kwargs):
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
        for _ in range(limit):
            color = board.current_player
            if simulation_policy == 'random':
                move = GoBoardUtil.generate_random_move(board,color)
           
        
            if move == PASS:
                break
            board.play_move(move, color)
        winner = GoBoardUtil.opponent(color)
        return winner

   