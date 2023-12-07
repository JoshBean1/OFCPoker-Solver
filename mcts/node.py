import copy
from mcts.scoring import score, royalty_points, notify_ftsyland
from itertools import combinations


class Node:
    def __init__(self, board1, board2, deck, hand=[], p1=True):
        self.board1 = board1
        self.board2 = board2
        self.deck = deck
        self.hand = hand
        self.p1 = p1

    def __str__(self):
        return str(self.board1) + '\n' + str(self.board2)

    def get_children(self):
        children_list = []
        self.deck.shuffle()
        if len(self.board1[0]) == 0 and len(self.board1[1]) == 0 and len(self.board1[2]) == 0:  # first turn, 5 cards
            '''
            5 0 0
            0 5 0
            4 1 0
            4 0 1
            0 4 1
            1 4 0
            3 2 0
            3 0 2
            0 3 2
            2 3 0
            2 0 3
            0 2 3
            2 2 1
            2 1 2
            1 2 2
            3 1 1
            1 3 1
            1 1 3
            '''
            if len(self.hand) == 0:
                for x in range(5):
                    self.hand.append(self.deck.deal_card())
            if len(self.hand) != 5:
                raise Exception("Starting hand needs 5 cards")

            four_combinations = []
            # Generate combinations of length 4
            for combo in combinations(self.hand, 4):
                # Find the remaining item
                remaining_item = [item for item in self.hand if item not in combo][0]
                # Append the combination along with the remaining item
                four_combinations.append(list(combo) + [remaining_item])
            three_combinations = []
            # Generate combinations of length 3
            for combo in combinations(self.hand, 3):
                # Find the remaining item
                remaining_items = [item for item in self.hand if item not in combo]
                # Append the combination along with the remaining item
                three_combinations.append(list(combo) + remaining_items)
            two_two_one_combinations = []
            for combo in combinations(self.hand, 2):
                remaining_three = [item for item in self.hand if item not in combo]
                for pair in combinations(remaining_three, 2):
                    remaining_item = [card for card in remaining_three if card not in pair][0]
                    two_two_one_combinations.append(list(combo) + list(pair) + [remaining_item])

            children_list.append(Node([self.hand, [], []], self.board2, self.deck))
            children_list.append(Node([[], self.hand, []], self.board2, self.deck))

            for combo in four_combinations:
                four = combo[0:4]
                one = [combo[-1]]
                children_list.append(Node([four, one, []], self.board2, self.deck))
                children_list.append(Node([four, [], one], self.board2, self.deck))
                children_list.append(Node([one, four, []], self.board2, self.deck))
                children_list.append(Node([[], four, one], self.board2, self.deck))

            for combo in three_combinations:
                three = combo[0:3]
                two = combo[3:5]
                fourth = [combo[3]]
                fifth = [combo[4]]
                children_list.append(Node([three, two, []], self.board2, self.deck))
                children_list.append(Node([three, [], two], self.board2, self.deck))
                children_list.append(Node([[], three, two], self.board2, self.deck))
                children_list.append(Node([two, three, []], self.board2, self.deck))
                children_list.append(Node([two, [], three], self.board2, self.deck))
                children_list.append(Node([[], two, three], self.board2, self.deck))
                children_list.append(Node([three, fourth, fifth], self.board2, self.deck))
                children_list.append(Node([fourth, three, fifth], self.board2, self.deck))
                children_list.append(Node([fourth, fifth, three], self.board2, self.deck))
                children_list.append(Node([three, fifth, fourth], self.board2, self.deck))
                children_list.append(Node([fifth, three, fourth], self.board2, self.deck))
                children_list.append(Node([fifth, fourth, three], self.board2, self.deck))

            for combo in two_two_one_combinations:
                first = combo[0:2]
                second = combo[2:4]
                last = combo[4:5]
                children_list.append(Node([first, second, last], self.board2, self.deck))
                children_list.append(Node([first, last, second], self.board2, self.deck))
                children_list.append(Node([last, first, second], self.board2, self.deck))

            return children_list

        elif not self.is_terminal():  # up to three possible children per card dealt
            if self.hand is None:
                card = self.deck.deal_card()
            else:
                card = self.hand[0]

            if len(self.board1[0]) < 5:
                children_list.append(Node([self.board1[0]+[card], self.board1[1][:], self.board1[2][:]], self.board2, self.deck))

            if len(self.board1[1]) < 5:
                children_list.append(Node([self.board1[0][:], self.board1[1]+[card], self.board1[2][:]], self.board2, self.deck))

            if len(self.board1[2]) < 3:
                children_list.append(Node([self.board1[0][:], self.board1[1][:], self.board1[2]+[card]], self.board2, self.deck))

            return children_list

    def random_playout(self, score_method='traditional'):
        board1_copy = [self.board1[0][:], self.board1[1][:], self.board1[2][:]]
        board2_copy = [self.board2[0][:], self.board2[1][:], self.board2[2][:]]
        deck_copy = copy.copy(self.deck)
        deck_copy.shuffle()

        while len(board1_copy[0]) < 5:
            board1_copy[0].append(deck_copy.deal_card())
        while len(board1_copy[1]) < 5:
            board1_copy[1].append(deck_copy.deal_card())
        while len(board1_copy[2]) < 3:
            board1_copy[2].append(deck_copy.deal_card())
        while len(board2_copy[0]) < 5:
            board2_copy[0].append(deck_copy.deal_card())
        while len(board2_copy[1]) < 5:
            board2_copy[1].append(deck_copy.deal_card())
        while len(board2_copy[2]) < 3:
            board2_copy[2].append(deck_copy.deal_card())

        if score_method == 'royalties':
            points = 0
            ftsy1, ftsy2 = notify_ftsyland(board1_copy, board2_copy)
            if ftsy1:
                points += 10  # approximate value of fantasyland
            points += royalty_points(board1_copy)
            return points
        else:
            points = 0
            ftsy1, ftsy2 = notify_ftsyland(board1_copy, board2_copy)
            if ftsy1:
                points += 10  # approximate value of fantasyland
            points += score(board1_copy, board2_copy)
            return points

    def score(self):
        if not self.is_terminal():
            raise Exception("Scoring cannot be completed on non-terminal node")
        return score(self.board1, self.board2)

    def is_terminal(self):
        if len(self.board1[0]) == 5 and len(self.board1[1]) == 5 and len(self.board1[2]) == 3:
            return True
        return False


class ChanceNode(Node):
    def __init__(self, node):
        # switch boards each layer, scoring function returns values only in terms of first player
        self.board2 = [node.board1[0][:], node.board1[1][:], node.board1[2][:]]
        self.board1 = [node.board2[0][:], node.board2[1][:], node.board2[2][:]]
        self.deck = copy.copy(node.deck)
        self.deck.shuffle()
        self.p1 = not node.p1

    def draw_child_list(self):
        chance_list = []

        if len(self.board1[0]) == 0 and len(self.board1[1]) == 0 and len(self.board1[2]) == 0:  # empty board
            for possible_draws in combinations(self.deck.deck, 5):
                children_list = []

                four_combinations = []
                # Generate combinations of length 4
                for combo in combinations(possible_draws, 4):
                    # Find the remaining item
                    remaining_item = [item for item in possible_draws if item not in combo][0]
                    # Append the combination along with the remaining item
                    four_combinations.append(list(combo) + [remaining_item])

                three_combinations = []
                # Generate combinations of length 3
                for combo in combinations(possible_draws, 3):
                    # Find the remaining item
                    remaining_items = [item for item in possible_draws if item not in combo]
                    # Append the combination along with the remaining item
                    three_combinations.append(list(combo) + remaining_items)

                two_two_one_combinations = []
                for combo in combinations(possible_draws, 2):
                    remaining_three = [item for item in possible_draws if item not in combo]
                    for pair in combinations(remaining_three, 2):
                        remaining_item = [card for card in remaining_three if card not in pair][0]
                        two_two_one_combinations.append(list(combo) + list(pair) + [remaining_item])

                children_list.append(Node([possible_draws, [], []], self.board2, self.deck, p1=self.p1))
                children_list.append(Node([[], possible_draws, []], self.board2, self.deck, p1=self.p1))

                for combo in four_combinations:
                    four = combo[0:4]
                    one = [combo[-1]]
                    children_list.append(Node([four, one, []], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([four, [], one], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([one, four, []], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([[], four, one], self.board2, self.deck, p1=self.p1))

                for combo in three_combinations:
                    three = combo[0:3]
                    two = combo[3:5]
                    fourth = [combo[3]]
                    fifth = [combo[4]]
                    children_list.append(Node([three, two, []], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([three, [], two], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([[], three, two], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([two, three, []], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([two, [], three], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([[], two, three], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([three, fourth, fifth], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([fourth, three, fifth], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([fourth, fifth, three], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([three, fifth, fourth], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([fifth, three, fourth], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([fifth, fourth, three], self.board2, self.deck, p1=self.p1))

                for combo in two_two_one_combinations:
                    first = combo[0:2]
                    second = combo[2:4]
                    last = combo[4:5]
                    children_list.append(Node([first, second, last], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([first, last, second], self.board2, self.deck, p1=self.p1))
                    children_list.append(Node([last, first, second], self.board2, self.deck, p1=self.p1))

                chance_list.append(children_list)

        elif not self.is_terminal():
            # random.shuffle(self.deck)
            for card in self.deck.deck:
                children_list = []
                deck_copy = copy.copy(self.deck)  # copy deck so that changes can be passed on to child nodes
                deck_copy.deck.remove(card)

                if len(self.board1[0]) < 5:
                    children_list.append(Node([self.board1[0] + [card], self.board1[1][:], self.board1[2][:]], [self.board2[0][:], self.board2[1][:], self.board2[2][:]], deck_copy, p1=self.p1))

                if len(self.board1[1]) < 5:
                    children_list.append(Node([self.board1[0][:], self.board1[1] + [card], self.board1[2][:]], [self.board2[0][:], self.board2[1][:], self.board2[2][:]], deck_copy, p1=self.p1))

                if len(self.board1[2]) < 3:
                    children_list.append(Node([self.board1[0][:], self.board1[1][:], self.board1[2] + [card]], [self.board2[0][:], self.board2[1][:], self.board2[2][:]], deck_copy, p1=self.p1))

                chance_list.append(children_list)

        return chance_list  # return random set of child node to simulate card draw
