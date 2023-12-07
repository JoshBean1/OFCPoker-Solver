from phevaluator import evaluate_cards, Deck, Card
from mcts.scoring import score, notify_fouls, notify_ftsyland
from mcts.node import Node
from mcts.mcts_closed import MCTS as mcts_closed
from mcts.mcts_open import MCTS as mcts_open
from mcts.fantasyland_solver import fantasyland, seq_solver
import time
import os


mcts_time = 5


def print_board(board):
    back = board[0]
    middle = board[1]
    front = board[2]
    back_row = ""
    middle_row = ""
    front_row = ""

    for card in back:
        back_row += str(card)
        if card != back[-1]:
            back_row += " "
    for x in range(5-len(back)):
        back_row += " _ "

    for card in middle:
        middle_row += str(card)
        if card != middle[-1]:
            middle_row += " "
    for x in range(5-len(middle)):
        middle_row += " _ "

    for card in front:
        front_row += str(card)
        if card != front[-1]:
            front_row += " "
    for x in range(3-len(front)):
        front_row += " _ "

    #print()
    print(front_row)
    print(middle_row)
    print(back_row)
    print()


def gen_node(board1, board2, deck, hand):
    return Node(board1, board2, deck, hand)


def manual_deal(deck):
    while True:
        deal = input("Card dealt: ")
        try:
            card = Card(deal)
        except:
            print("Invalid card, format should be '2h', 'Ts', 'Qc', etc.")
            continue
        try:
            deck.deck.remove(card)
        except:
            print("Card already dealt")
            continue
        break
    return card


def play_turn(player, board1, board2, deck, hand):
    global mcts_time
    print("Opponent's Board:")
    print_board(board2)
    if player == "1":
        print("Your Board:")
    elif player == "2":
        print("Computer's board:")
    print_board(board1)
    if player == "1":  # person
        hand_str = ""
        for card in hand:
            hand_str += " " + str(card) + " "
        for card in hand:
            print("Hand:", hand_str)
            print("Place card: " + str(card))
            print("Back row = 1, middle = 2, front = 3")
            while True:
                placement = input("Input row to place: ")
                try:
                    placement = int(placement)
                    if (placement == 1 and len(board1[0]) < 5) or (placement == 2 and len(board1[1]) < 5) or (placement == 3 and len(board1[2]) < 3):
                        break
                    else:
                        print("Row is full")
                except:
                    continue

            board1[(int(placement)-1)].append(card)
            clear_screen()
            print("Opponent's Board:")
            print_board(board2)
            print("Your Board:")
            print_board(board1)

        return board1

    else:  # AI
        # check for two of three rows filled to save time
        runtime = mcts_time
        node = gen_node(board1, board2, deck, hand)
        hand_str = ""
        for card in hand:
            hand_str += " " + str(card)
        print(f"Dealt {hand_str}, computer thinking...")
        time.sleep(0.5)

        if len(node.get_children()) == 1:
            return node.get_children()[0].board1

        if board_empty(board1):
            mcts = mcts_open(node)
            runtime = 12
        else:
            mcts = mcts_closed(node)
        start_time = time.time()
        # Run the while loop until the desired duration is reached
        while time.time() - start_time < runtime:
            mcts.rollout()
        choice = mcts.choose()
        return choice.board1


def board_empty(board):
    if len(board[0]) == 0 and len(board[1]) == 0 and len(board[2]) == 0:
        return True
    return False


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def boards_full(board1, board2):
    if len(board1[0]) == 5 and len(board1[1]) == 5 and len(board1[2]) == 3 and len(board2[0]) == 5 and len(board2[1]) == 5 and len(board2[2]) == 3:
        return True
    return False


def board_full(board):
    if len(board[0]) == 5 and len(board[1]) == 5 and len(board[2]) == 3:
        return True
    return False


def play_ftsyland(player1, player2, ftsyland):
    repeat_flag1, repeat_flag2 = False, False
    board1 = [[], [], []]
    board2 = [[], [], []]
    hand1 = []
    hand2 = []
    deck = Deck()
    deck.shuffle()
    if ftsyland[0]:  # player 1 qualifies
        for x in range(13):
            hand1.append(deck.deal_card())
        board1, repeat_flag1 = fantasyland(hand1)
    else:  # sees cards one at a time
        if player1 == '1':
            print("Your Board:")
            print_board(board1)
            while not board_full(board1):
                hand1 = []
                if board_empty(board1):
                    for x in range(5):
                        hand1.append(deck.deal_card())
                else:
                    hand1.append(deck.deal_card())

                hand_str = ""
                for card in hand1:
                    hand_str += " " + str(card) + " "
                for card in hand1:
                    print("Hand:", hand_str)
                    print("Place card: " + str(card))
                    print("Back row = 1, middle = 2, front = 3")
                    while True:
                        placement = input("Input row to place: ")
                        try:
                            placement = int(placement)
                            if (placement == 1 and len(board1[0]) < 5) or (placement == 2 and len(board1[1]) < 5) or (placement == 3 and len(board1[2]) < 3):
                                break
                            else:
                                print("Row is full")
                        except:
                            continue

                    board1[(int(placement) - 1)].append(card)
                    clear_screen()
                    print("Your Board:")
                    print_board(board1)
        else:
            while not board_full(board1):
                hand1 = []
                if board_empty(board1):
                    for x in range(5):
                        hand1.append(deck.deal_card())
                else:
                    hand1.append(deck.deal_card())
                print("Computer board:")
                print_board(board1)
                board1 = seq_solver(board1, hand1, deck)
                clear_screen()

    if ftsyland[1]:  # player 2 qualifies
        for x in range(13):
            hand2.append(deck.deal_card())
        board2, repeat_flag2 = fantasyland(hand2)
    else:
        if player2 == '1':
            print("Your Board:")
            print_board(board2)
            while not board_full(board2):
                hand2 = []
                if board_empty(board2):
                    for x in range(5):
                        hand2.append(deck.deal_card())
                else:
                    hand2.append(deck.deal_card())

                hand_str = ""
                for card in hand2:
                    hand_str += " " + str(card) + " "
                for card in hand2:
                    print("Hand:", hand_str)
                    print("Place card: " + str(card))
                    print("Back row = 1, middle = 2, front = 3")
                    while True:
                        placement = input("Input row to place: ")
                        try:
                            placement = int(placement)
                            if (placement == 1 and len(board1[0]) < 5) or (placement == 2 and len(board1[1]) < 5) or (placement == 3 and len(board1[2]) < 3):
                                break
                            else:
                                print("Row is full")
                        except:
                            continue

                    board2[(int(placement) - 1)].append(card)
                    clear_screen()
                    print("Your Board:")
                    print_board(board2)
        else:
            while not board_full(board2):
                hand2 = []
                if board_empty(board2):
                    for x in range(5):
                        hand2.append(deck.deal_card())
                else:
                    hand2.append(deck.deal_card())
                print("Computer board:")
                print_board(board2)
                board2 = seq_solver(board2, hand2, deck)
                clear_screen()
    print("Player 1 board:")
    print_board(board1)
    print("Player 2 board:")
    print_board(board2)

    return score(board1, board2), (repeat_flag1, repeat_flag2)


def play_hand(player1, player2, p1_button, deal):
    board1 = [[], [], []]
    board2 = [[], [], []]
    deck = Deck()
    deck.shuffle()

    while not boards_full(board1, board2):
        if not p1_button:
            hand1 = []
            hand2 = []

            if board_empty(board1):
                for x in range(5):
                    if deal == 'y':
                        hand1.append(manual_deal(deck))
                    else:
                        hand1.append(deck.deal_card())
            else:
                if deal == 'y':
                    hand1.append(manual_deal(deck))
                else:
                    hand1.append(deck.deal_card())

            board1 = play_turn(player1, board1, board2, deck, hand1)
            clear_screen()

            if board_empty(board2):
                for x in range(5):
                    if deal == 'y':
                        hand2.append(manual_deal(deck))
                    else:
                        hand2.append(deck.deal_card())
            else:
                if deal == 'y':
                    hand2.append(manual_deal(deck))
                else:
                    hand2.append(deck.deal_card())
            board2 = play_turn(player2, board2, board1, deck, hand2)
            if not boards_full(board1, board2):
                clear_screen()
        else:
            hand1 = []
            hand2 = []

            if board_empty(board2):
                for x in range(5):
                    if deal == 'y':
                        hand2.append(manual_deal(deck))
                    else:
                        hand2.append(deck.deal_card())
            else:
                if deal == 'y':
                    hand2.append(manual_deal(deck))
                else:
                    hand2.append(deck.deal_card())
            board2 = play_turn(player2, board2, board1, deck, hand2)
            clear_screen()

            if board_empty(board1):
                for x in range(5):
                    if deal == 'y':
                        hand1.append(manual_deal(deck))
                    else:
                        hand1.append(deck.deal_card())
            else:
                if deal == 'y':
                    hand1.append(manual_deal(deck))
                else:
                    hand1.append(deck.deal_card())
            board1 = play_turn(player1, board1, board2, deck, hand1)
            if not boards_full(board1, board2):
                clear_screen()
    return score(board1, board2), notify_fouls(board1, board2), notify_ftsyland(board1, board2)


def main():
    p1_score = 0
    p2_score = 0
    p1_button = True  # player 1 goes last

    while True:
        player1 = input("Player 1 - human (1) or computer (2)? ")
        if player1 == "1" or player1 == "2":
            break
    while True:
        player2 = input("Player 2 - human (1) or computer (2)? ")
        if player2 == "1" or player2 == "2":
            break

    while True:
        deal = input("Deal cards manually? (y/n) ")
        if deal == "y" or deal == "n":
            break

    print("GAME START...")
    time.sleep(2)
    clear_screen()

    while True:
        points, fouls, ftsyland = play_hand(player1, player2, p1_button, deal)
        #points, fouls, ftsyland = 0, (False, False), (True, False)
        p1_score += points
        p2_score -= points

        if fouls[0]:
            print("Player 1 fouled")
        if fouls[1]:
            print("Player 2 fouled")

        if ftsyland[0]:
            print("Player 1 qualifies for 'fantasyland'")
        if ftsyland[1]:
            print("Player 2 qualifies for 'fantasyland'")

        while ftsyland[0] or ftsyland[1]:
            points, ftsyland = play_ftsyland(player1, player2, ftsyland)

            p1_score += points
            p2_score -= points

        print("Player 1 score: " + str(p1_score))
        print("Player 2 score: " + str(p2_score) + "\n")

        while True:
            ans = input("Would you like to play another hand? (y/n): ")
            if ans.lower() == 'y':
                p1_button = not p1_button
                break
            elif ans.lower() == 'n':
                exit()
            else:
                print('invalid')


main()
