import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python camel_cards.py input.txt')

    with open(sys.argv[1]) as input_file:
        lines = input_file.readlines()

    # clean up the last line to not have to do it when looping over the
    # hand - bids
    if lines[-1] == '\n':
        lines = lines[:-1]

    # card_labels contain all possible cards in game, use the index for strength of
    # card comparison, I know it's O(n) but for a list that has 13 items shouldn't
    # be an issue, if there were far more possible card types would've made a dict
    card_labels = ['2', '3', '4', '5', '6',
                   '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    # changed my mind, let's just make a dict, make the values for each key be the
    # index of the value in card_labels, if index(a) > index(b) then a has a higher
    # strength
    card_value_dict = {}
    for card_idx, card in enumerate(card_labels):
        card_value_dict[card] = card_idx

    # need to loop over the list of hands, and sort them from worst to best
    # then multiply it's bid by it's rank, rank 1 being the worst hand, to do
    # this, want to place each line into a tuple, then split hands into one of
    # 7 hand types. each hand needs to remain as written because
    # card order matters for tie breaks.

    # loop over hands, turn to tuple, place in appropriate sublist
    hand_types = {
        'five_kind': [],
        'four_kind': [],
        'full_house': [],
        'three_kind': [],
        'two_pair': [],
        'one_pair': [],
        'high_card': [],
    }

    for line in lines:
        temp = line.split()
        tupled = (temp[0], temp[1])
        if is_five_kind(tupled[0]):
            hand_types['five_kind'].append(tupled)
            continue
        elif is_four_kind(tupled[0]):
            hand_types['four_kind'].append(tupled)
            continue
        elif is_full_house(tupled[0]):
            hand_types['full_house'].append(tupled)
            continue
        elif is_three_kind(tupled[0]):
            hand_types['three_kind'].append(tupled)
            continue
        elif is_two_pair(tupled[0]):
            hand_types['two_pair'].append(tupled)
            continue
        elif is_one_pair(tupled[0]):
            hand_types['one_pair'].append(tupled)
            continue
        else:
            hand_types['high_card'].append(tupled)

    for key in hand_types:
        hand_types[key] = sort_sublist(hand_types[key], card_value_dict)

    # Once the hands are sorted from smallest strength to largest,
    # combine them all from weakest kind to strongest kind.
    master_list = (hand_types['high_card'] +
                   hand_types['one_pair'] +
                   hand_types['two_pair'] +
                   hand_types['three_kind'] +
                   hand_types['full_house'] +
                   hand_types['four_kind'] +
                   hand_types['five_kind'])

    total_bid = 0

    for rank, tuples in enumerate(master_list):
        total_bid += int(tuples[1]) * (int(rank) + 1)

    print(total_bid)
    return total_bid


def sort_sublist(list_of_tuples, values_dict):
    # Given a list of tuples containing a hand and it's bid
    # sort by strength of the hand and then return a sorted
    # list, will use bubblesort
    new_list = list_of_tuples
    for i, tupled in enumerate(new_list):
        for j in range(len(new_list) - i - 1):
            # get the value of a given card in a hand until
            # one wins out, 5 cards per hand
            for card in range(5):
                if (values_dict[new_list[j][0][card]] ==
                        values_dict[new_list[j + 1][0][card]]):
                    continue
                elif (values_dict[new_list[j][0][card]] <
                        values_dict[new_list[j + 1][0][card]]):
                    break
                elif (values_dict[new_list[j][0][card]] >
                        values_dict[new_list[j + 1][0][card]]):
                    new_list[j],  new_list[j +
                                           1] = new_list[j + 1],  new_list[j]
                    break

    return new_list


def is_five_kind(hand):
    if hand == hand[0] * len(hand):
        return True
    return False


def is_four_kind(hand):
    return any([i for i in hand if hand.count(i) == 4])


def is_full_house(hand):
    char_1 = []
    char_2 = []
    for char in hand:
        if char_1 == []:
            char_1.append(char)
        elif char == char_1[0]:
            char_1.append(char)
        elif char_2 == []:
            char_2.append(char)
        elif char == char_2[0]:
            char_2.append(char)
        else:
            # if it reaches here there is a third
            # type of card so cannot be full house
            return False
    # double check that one list is len 2 and the other is 3
    return ((len(char_1) == 3 and len(char_2) == 2)
            or (len(char_1) == 2 and len(char_2) == 3))


def is_three_kind(hand):
    return any([i for i in hand if hand.count(i) == 3])


def is_two_pair(hand):
    char_1 = []
    char_2 = []
    char_3 = []
    for char in hand:
        if char_1 == []:
            char_1.append(char)
        elif char == char_1[0]:
            char_1.append(char)
        elif char_2 == []:
            char_2.append(char)
        elif char == char_2[0]:
            char_2.append(char)
        elif char_3 == []:
            char_3.append(char)
        elif char == char_3[0]:
            char_3.append(char)
        else:
            # if it reaches here there is a third
            # type of card so cannot be full house
            return False
    # double check that one list is len 2 and the other is 3
    return ((len(char_1) == 2 and len(char_2) == 2) or
            (len(char_1) == 2 and len(char_3) == 2) or
            (len(char_2) == 2 and len(char_3) == 2))


def is_one_pair(hand):
    # WARNING THIS WILL RETURN TRUE FOR MULTIPLE PAIRS,
    # NOT MEANT TO BE CALLED BEFORE is_two_pair(hand)
    return any([i for i in hand if hand.count(i) == 2])


if __name__ == "__main__":
    # list_tuple = [('QQQJA', '483'), ('T55J5', '684')]
    # card_labels = ['2', '3', '4', '5', '6',
    #               '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    # changed my mind, let's just make a dict, make the values for each key be the
    # index of the value in card_labels, if index(a) > index(b) then a has a higher
    # strength
    # card_value_dict = {}
    # for card_idx, card in enumerate(card_labels):
    #    card_value_dict[card] = card_idx
    # print(card_value_dict)
    # print(sort_sublist(list_tuple, card_value_dict))

    # new test_input expected output: for pt1: 6592 for pt2: 6839

    main()
