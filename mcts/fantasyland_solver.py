from itertools import combinations
from mcts.mcts_ftsyland import MCTS
from mcts.node_ftsyland import Node
import phevaluator
from mcts import scoring
import time


def fantasyland(hand):
    repeat_flag = False
    combinations_5_5_3 = []
    # make list of possible hands from 13 cards
    for comb_5_1 in combinations(hand, 5):
        remaining_cards = [card for card in hand if card not in comb_5_1]
        for comb_5_2 in combinations(remaining_cards, 5):
            comb_3 = [item for item in remaining_cards if item not in comb_5_2]
            combinations_5_5_3.append((list(comb_5_1), list(comb_5_2), list(comb_3)))

    # filter out fouling boards
    valid_combos = []
    for combo in combinations_5_5_3:  #
        back = phevaluator.evaluate_cards(*combo[0])
        middle = phevaluator.evaluate_cards(*combo[1])
        front = phevaluator.evaluate_cards(*combo[2])
        if not (back <= middle <= front):
            continue
        valid_combos.append(combo)

    # look for hands that stay in fantasyland
    ftsy_land_hands = []

    for hand in valid_combos:
        if scoring.get_royalty(phevaluator.evaluate_cards(*hand[0]), "BACK") >= 10 or scoring.get_royalty(phevaluator.evaluate_cards(*hand[1]), "MIDDLE") >= 10 or scoring.get_royalty(phevaluator.evaluate_cards(*hand[2]), "FRONT") >= 10:
            ftsy_land_hands.append(hand)

    # find best fantsyland option if possible
    def best_score(hand):
        return phevaluator.evaluate_cards(*hand[0]) + phevaluator.evaluate_cards(*hand[1]) + phevaluator.evaluate_cards(*hand[2])
    if len(ftsy_land_hands) != 0:
        repeat_flag = True
        return min(ftsy_land_hands, key=best_score), repeat_flag
    else:
        return min(valid_combos, key=best_score), repeat_flag


def seq_solver(board, hand, deck):
    node = Node(board1=board, deck=deck, hand=hand)

    if len(node.get_children()) == 1:
        return node.get_children()[0].board1

    if len(board[0]) == 0 and len(board[1]) == 0 and len(board[2]) == 0:
        scoring = 'royalties'
    else:
        scoring = 'traditional'

    mcts = MCTS(node)

    start_time = time.time()
    while time.time() - start_time < 10:
        mcts.rollout(sims=1, score_method=scoring)
    return mcts.choose_max().board1

