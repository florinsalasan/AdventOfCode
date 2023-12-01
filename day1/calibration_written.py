import sys


def main():
    if (len(sys.argv)) != 2:
        sys.exit('Usage: python calibration_written.py calibration_document')

    # Want the same functionality as other calibration doc but this want to
    # be able to spot the digits spelled out so if the line contains 'six'
    # and it is either the first or the last digit it counts, 'six78seven9'
    # would give 6 and 9 as the first and last digit and combine to
    # 69 to be added to the running sum.

    with open(sys.argv[1]) as cali_doc:
        lines = cali_doc.readlines()

    # file = open('test_calibrate.txt')
    # lines = file.readlines()
    # file.close()

    # Create a dictionary that contains a list of possible numbers
    # that can be spelled out with a given starting letter
    # only includes values from 1 - 9 inclusive, 'zero' wasn't
    # taken into consideration according to the specs and it
    # is not in the calibration_doc either, only want to check
    # letters that are keys in this dictionary rather than every
    # single one that is not a digit

    digit_dict = {
        'o': {'one': [3, 1]},  # Want the list to have the length, then value
        't': {'two': [3, 2], 'three': [5, 3]},
        'f': {'four': [4, 4], 'five': [4, 5]},
        's': {'six': [3, 6], 'seven': [5, 7]},
        'e': {'eight': [5, 8]},
        'n': {'nine': [4, 9]}
    }

    sum = 0

    for line in lines:
        if line == lines[-1]:
            break
        first_digit = None
        second_digit = None

        for i in range(len(line)):
            if line[i].isdigit():
                if first_digit is None:
                    first_digit = int(line[i])
                second_digit = int(line[i])
            elif line[i] in list(digit_dict.keys()):
                sub_dict = digit_dict[line[i]]
                for key in list(sub_dict.keys()):
                    if line[i: i + sub_dict[key][0]] == key:
                        # if reached then the substring is a digit spelled out
                        # so get the value from the sub_dict and modify i
                        if first_digit is None:
                            first_digit = sub_dict[key][1]
                        else:
                            second_digit = sub_dict[key][1]
                        i += sub_dict[key][0]

        if second_digit is None:
            second_digit = first_digit

        sum += (first_digit * 10) + second_digit

        # line[i] is the key for digit_dict, so digit_dict[line[i]] should return {'one': [3, 1]} if line[i] == 'o';
        # thus digit_dict[line[i]][key] should give [3, 1]

    print(sum)
    return sum


if __name__ == "__main__":
    main()
