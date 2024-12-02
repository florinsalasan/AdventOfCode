import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python3 possible.py puzzle_input')
    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    total_passing = 0
    for line in lines:
        list_line = line.split(" ")
        if is_descending(list_line) or is_ascending(list_line):
            total_passing += 1

    print(total_passing)
    return total_passing


def is_descending(input_list):
    for i in range(1, len(input_list)):
        should_be_bigger = int(input_list[i - 1])
        comparison_value = int(input_list[i])
        if (should_be_bigger <= comparison_value or
                should_be_bigger - comparison_value > 3):
            return False

    return True


def is_ascending(input_list):
    for i in range(1, len(input_list)):
        should_be_smaller = int(input_list[i - 1])
        comparison_value = int(input_list[i])
        if (should_be_smaller >= comparison_value or
                comparison_value - should_be_smaller > 3):
            return False

    return True


if __name__ == '__main__':
    main()
