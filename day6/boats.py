import sys


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
        new_lines.append(listed_line)

    # match the record to the race length:
    len_to_record = {}
    for i, race_len in enumerate(new_lines[0]):
        if not race_len.isdigit():
            continue
        len_to_record[int(race_len)] = int(new_lines[1][i])

    # have a dictionary mapping the race length to race record, now find
    # all button presses that would beat the record for a given length
    product = 1
    for race_len in len_to_record.keys():
        product *= ways_to_beat_record(race_len, len_to_record[race_len])
    print(product)
    return product


def ways_to_beat_record(race_len, record_dist):
    count = 0
    for x in range(race_len + 1):
        distance = (race_len - x)*x
        if distance > record_dist:
            count += 1
    return count


if __name__ == "__main__":
    main()
