import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python3 possible.py puzzle_input')
    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    total_passing = 0
    collection_passing = []
    for line in lines:
        list_line = line.split(" ")
        int_line = []
        for item in list_line:
            int_line.append(int(item))
        if is_descending(int_line, True) or is_ascending(int_line, True):
            total_passing += 1
            collection_passing.append(int_line)

    for passing_list in collection_passing:
        print(passing_list)
    print(total_passing)
    return total_passing


def is_descending(input_list, base_list):
    list_len = len(input_list)
    for i in range(1, list_len):
        should_be_bigger = input_list[i - 1]
        comparison_value = input_list[i]
        if (should_be_bigger <= comparison_value or
                should_be_bigger - comparison_value > 3) and base_list:
            # If we reach this point we need to check if any sublist with
            # one item removed would pass probably ideal to remove at the
            # index where it fails
            sublists = [is_descending(input_list[:j] + input_list[j + 1:], False) for
                        j in range(list_len)]
            return any(sublists)

        elif (should_be_bigger <= comparison_value or
                should_be_bigger - comparison_value > 3) and not base_list:
            return False

    return True


def is_ascending(input_list, base_list):
    list_len = len(input_list)
    for i in range(1, list_len):
        should_be_smaller = input_list[i - 1]
        comparison_value = input_list[i]
        if (should_be_smaller >= comparison_value or
                comparison_value - should_be_smaller > 3) and base_list:
            # If we reach this point we need to check if any sublist with
            # one item removed would pass probably ideal to remove at the
            # index where it fails
            sublists = [is_ascending(input_list[:j] + input_list[j + 1:], False) for
                        j in range(list_len)]
            return any(sublists)

        elif (should_be_smaller >= comparison_value or
                comparison_value - should_be_smaller > 3) and not base_list:
            return False

    return True


if __name__ == '__main__':
    main()
