import sys
import math


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python boats.py tournament_records.txt')

    with open(sys.argv[1]) as tournament_records:
        lines = tournament_records.readlines()

    if (len(lines) != 2):
        sys.exit('input file should have two lines, first being the length of the race and the second being the record length')

    new_lines = []
    for line in lines:
        listed_line = line.split()
        listed_line = listed_line[1:]
        joined = ''.join(listed_line)
        new_lines.append(joined)

    print(new_lines)
    race_len = int(new_lines[0])
    record_dist = int(new_lines[1])
    print(race_len, record_dist)
    # probably should not try to brute force an input of ~35 million
    # distance = (race_len - x) * x where x is time the button is held for,
    # solve for such that distance > record_distance
    # so record_distance < (race_len - x) * x
    # record_distance < x*race_len - x^2
    # 212206012011044 < 35937366x - x^2
    # x^2 - 35937366x + 212206012011044 < 0
    ########
    # Was being dumb again, just solve for the roots where the inequality is 0,
    # should usually solve for a value in between the roots to know if the values
    # in between the roots are positive or negative, but in this case in between
    # should be above 0 since it is unreasonable to count an infinite number of ways
    # to beat the record distance
    # so solve x^2 - 35937366x + 212206012011044 = 0
    ########
    # Once again my genius frightens me, just get the roots with:
    # (-b +/- sqrt(b^2 - 4ac))/2a kinda crazy how much basic math
    # you can forget if you don't use it regularly
    x_1 = int((race_len + math.sqrt((race_len**2) - 4*record_dist))/2)
    x_2 = int((race_len - math.sqrt((race_len**2) - 4*record_dist))/2)

    print(x_1, x_2)

    x_1_wins = beats_record(x_1, race_len, record_dist)
    x_2_wins = beats_record(x_2, race_len, record_dist)

    range_solutions = x_1 - x_2 + 1  # count roots inclusively
    if not x_2_wins:
        range_solutions -= 1
    if not x_1_wins:
        range_solutions -= 1

    print(range_solutions)
    return range_solutions


def beats_record(given_x, race_len, record_dist):
    if (race_len - given_x) * given_x > record_dist:
        return True
    return False


if __name__ == "__main__":
    main()
