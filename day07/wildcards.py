import sys
# So in this one the card values get changed, J is a wildcard
# which can create the best possible hand, so for example:
# 'AJJA3' is no longer two pair, it would be 4 of a kind,
# However 'AAAA3' beats it because J is no longer a strong
# card it is the weakest in a head to head tiebreak.


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
    card_labels = ['J', '2', '3', '4', '5', '6',
                   '7', '8', '9', 'T', 'Q', 'K', 'A']
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
        num_js = count_wildcards(temp[0])
        # WARNING DO NOT CHANGE THE ORDER OF THESE FUNCTION CALLS
        # THEY DO NOT NECESSARILY ONLY RETURN IF TRUE, MORE LIKE
        # THEY ARE TRUE IF AT LEAST 4 OF A KIND, so is_four_kind
        # returns true for 'AAAAA' and 'AAKAA', not 'AAKKQ'
        # 'AAKKQ' would be true for both two and one pair.
        if is_five_kind(tupled[0], num_js):
            hand_types['five_kind'].append(tupled)
            continue
        elif is_four_kind(tupled[0], num_js):
            hand_types['four_kind'].append(tupled)
            continue
        elif is_full_house(tupled[0], num_js):
            hand_types['full_house'].append(tupled)
            continue
        elif is_three_kind(tupled[0], num_js):
            hand_types['three_kind'].append(tupled)
            continue
        elif is_two_pair(tupled[0], num_js):
            hand_types['two_pair'].append(tupled)
            continue
        elif is_one_pair(tupled[0], num_js):
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
    print(master_list)

    for rank, tuples in enumerate(master_list):
        total_bid += int(tuples[1]) * (int(rank) + 1)

    print(total_bid)
    return total_bid


def count_wildcards(hand):
    return hand.count('J')


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


def is_five_kind(hand, num_js):
    if num_js == 5:
        return True
    to_modify = list(hand)
    for i in range(num_js):
        to_modify.remove('J')
    to_modify = ''.join(to_modify)
    return to_modify == to_modify[0] * len(to_modify)


def is_four_kind(hand, num_js):
    to_modify = list(hand)
    for i in range(num_js):
        to_modify.remove('J')
    to_modify = ''.join(to_modify)
    return any([i for i in to_modify if to_modify.count(i) >= 4 - num_js])


def is_full_house(hand, num_js):
    to_modify = list(hand)
    for i in range(num_js):
        to_modify.remove('J')
    to_modify = ''.join(to_modify)

    char_1 = []
    char_2 = []
    for char in to_modify:
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
            # even after removing the wildcardshand
            return False
    # if there are only two character types in the
    # modified list, return True, not because it is
    # always a full house, but if it wasn't it should
    # have been caught earlier and placed in either
    # four or five of a kind.
    return True


def is_three_kind(hand, num_js):
    return any([i for i in hand if hand.count(i) >= 3 - num_js])


def is_two_pair(hand, num_js):
    to_modify = list(hand)
    for i in range(num_js):
        to_modify.remove('J')
    to_modify = ''.join(to_modify)

    char_1 = []
    char_2 = []
    char_3 = []
    for char in to_modify:
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
            # type of card so cannot be a two pair with 4 chars
            return False
    # When you reach here the wildcards are removed and any of the
    # remaining characters are placed in one of 3 lists, if I check that the
    # length of any two lists plus the num of js is at least 4 that should be good
    # enough to show that there is a pair, I believe. 'AQQQ3' would return true on
    # two pair BUT should have been caught already by 3 of a kind, so shouldn't matter.
    # Can't think of an input that would not be a higher strength hand, that would
    # fail this check
    return any([(len(char_1) + len(char_2) + num_js >= 4),
                (len(char_1) + len(char_3) + num_js >= 4),
                (len(char_3) + len(char_2) + num_js >= 4)])


def is_one_pair(hand, num_js):
    # WARNING THIS WILL RETURN TRUE FOR MULTIPLE PAIRS,
    # NOT MEANT TO BE CALLED BEFORE is_two_pair(hand)
    if num_js > 0:
        return True
    return any([i for i in hand if hand.count(i) == 2])


if __name__ == "__main__":
    print(is_four_kind('T55J5', 1))
    print(is_four_kind('Q2KJJ', 2))
    main()
