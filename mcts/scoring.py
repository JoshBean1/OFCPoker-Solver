import phevaluator
# Trips: 2467, Straight: 1609, Flush: 1599, Full House: 322, Quads: 166, Straight Flush: 10, Royal Flush: 1


def get_royalty(strength, row):
    row = row.upper()
    if row == "BACK":
        if 1609 >= strength >= 1600:  # straight
            return 2
        elif 1599 >= strength >= 323:  # flush
            return 4
        elif 322 >= strength >= 167:  # full house
            return 6
        elif 166 >= strength >= 11:  # quads
            return 10
        elif 10 >= strength >= 2:  # straight flush
            return 15
        elif strength == 1:  # royal
            return 25
        else:
            return 0

    elif row == "MIDDLE":
        if 2467 >= strength >= 1610:  # trips
            return 2
        elif 1609 >= strength >= 1600:  # straight
            return 4
        elif 1599 >= strength >= 323:  # flush
            return 8
        elif 322 >= strength >= 167:  # full house
            return 12
        elif 166 >= strength >= 11:  # quads
            return 20
        elif 10 >= strength >= 2:  # straight flush
            return 30
        elif strength == 1:  # royal
            return 50
        else:
            return 0

    elif row == "FRONT":  # 3 card hand
        if 5305 >= strength >= 5086:  # pair 6's
            return 1
        elif 5085 >= strength >= 4866:  # pair 7's
            return 2
        elif 4865 >= strength >= 4646:  # pair 8's
            return 3
        elif 4645 >= strength >= 4426:  # pair 9's
            return 4
        elif 4425 >= strength >= 4206:  # pair 10's
            return 5
        elif 4205 >= strength >= 3986:  # pair J's
            return 6
        elif 3985 >= strength >= 3766:  # pair Q's
            return 7
        elif 3765 >= strength >= 3546:  # pair K's
            return 8
        elif 3545 >= strength >= 2468:  # pair A's
            return 9
        elif strength == 2467:  # trip 2's
            return 10
        elif strength == 2401:  # trip 3's
            return 11
        elif strength == 2335:  # trip 4's
            return 12
        elif strength == 2269:  # trip 5's
            return 13
        elif strength == 2203:  # trip 6's
            return 14
        elif strength == 2137:  # trip 7's
            return 15
        elif strength == 2071:  # trip 8's
            return 16
        elif strength == 2005:  # trip 9's
            return 17
        elif strength == 1939:  # trip 10's
            return 18
        elif strength == 1873:  # trip J's
            return 19
        elif strength == 1807:  # trip Q's
            return 20
        elif strength == 1741:  # trip K's
            return 21
        elif strength == 1675:  # trip A's
            return 22
        else:
            return 0

    else:
        raise Exception(f"Row should be 'BACK', 'MIDDLE', or 'FRONT'\nrow = {row}")


def score(board1, board2):  # board should be list of rows - back, middle, front
    player1 = 0
    player2 = 0
    p1Back = phevaluator.evaluate_cards(*board1[0])
    p1Mid = phevaluator.evaluate_cards(*board1[1])
    p1Front = phevaluator.evaluate_cards(*board1[2])
    p2Back = phevaluator.evaluate_cards(*board2[0])
    p2Mid = phevaluator.evaluate_cards(*board2[1])
    p2Front = phevaluator.evaluate_cards(*board2[2])

    # if hand fouls
    if not(p1Back <= p1Mid <= p1Front):
        p1Back = float('inf')
        p1Mid = float('inf')
        p1Front = float('inf')
    if not(p2Back <= p2Mid <= p2Front):
        p2Back = float('inf')
        p2Mid = float('inf')
        p2Front = float('inf')

    # point for winning rows
    if p1Back < p2Back:
        player1 += 1
    if p1Mid < p2Mid:
        player1 += 1
    if p1Front < p2Front:
        player1 += 1
    # scoop bonus
    if player1 == 3:
        player1 += 3

    player1 += get_royalty(p1Back, "BACK")
    player1 += get_royalty(p1Mid, "MIDDLE")
    player1 += get_royalty(p1Front, "FRONT")

    # point for winning rows
    if p2Back < p1Back:
        player2 += 1
    if p2Mid < p1Mid:
        player2 += 1
    if p2Front < p1Front:
        player2 += 1
    # scoop bonus
    if player2 == 3:
        player2 += 3

    player2 += get_royalty(p2Back, "BACK")
    player2 += get_royalty(p2Mid, "MIDDLE")
    player2 += get_royalty(p2Front, "FRONT")

    #return get_royalty(p1Back, "BACK")+get_royalty(p1Mid, "MIDDLE")+get_royalty(p1Front, "FRONT")
    return player1 - player2


def notify_fouls(board1, board2):
    p1foul = False
    p2foul = False
    p1Back = phevaluator.evaluate_cards(*board1[0])
    p1Mid = phevaluator.evaluate_cards(*board1[1])
    p1Front = phevaluator.evaluate_cards(*board1[2])
    p2Back = phevaluator.evaluate_cards(*board2[0])
    p2Mid = phevaluator.evaluate_cards(*board2[1])
    p2Front = phevaluator.evaluate_cards(*board2[2])

    # if hand fouls
    if not (p1Back <= p1Mid <= p1Front):
        p1foul = True
    if not (p2Back <= p2Mid <= p2Front):
        p2foul = True

    return p1foul, p2foul


def notify_ftsyland(board1,board2):
    p1_ftsy = False
    p2_ftsy = False
    p1Back = phevaluator.evaluate_cards(*board1[0])
    p1Mid = phevaluator.evaluate_cards(*board1[1])
    p1Front = phevaluator.evaluate_cards(*board1[2])
    p2Back = phevaluator.evaluate_cards(*board2[0])
    p2Mid = phevaluator.evaluate_cards(*board2[1])
    p2Front = phevaluator.evaluate_cards(*board2[2])

    # if hand fouls
    if not (p1Back <= p1Mid <= p1Front):
        p1Front = float('inf')
    if not (p2Back <= p2Mid <= p2Front):
        p2Front = float('inf')

    front1 = get_royalty(p1Front, "FRONT")
    front2 = get_royalty(p2Front, "FRONT")

    if front1 >= 7:
        p1_ftsy = True
    if front2 >= 7:
        p2_ftsy = True
    return p1_ftsy, p2_ftsy


def royalty_points(board):  # function to make solver select more aggressive strategy for first 5 cards in hand
    player1 = 0
    back = phevaluator.evaluate_cards(*board[0])
    middle = phevaluator.evaluate_cards(*board[1])
    front = phevaluator.evaluate_cards(*board[2])

    if not(back <= middle <= front):
        return 0

    player1 += get_royalty(back, "BACK")
    player1 += get_royalty(middle, "MIDDLE")
    player1 += get_royalty(front, "FRONT")

    return player1


def ftsyland_score(board):
    back = phevaluator.evaluate_cards(*board[0])
    mid = phevaluator.evaluate_cards(*board[1])
    front = phevaluator.evaluate_cards(*board[2])
    # 7462 is worst rank
    if not (back <= mid <= front):
        back = 7462
        mid = 7462
        front = 7462

    return back + mid + front  # ftsyland solver tries to maximize overall hand strength
