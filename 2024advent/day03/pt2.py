import sys
import re


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python3 pt1.py puzzle_input')
    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    giga_line = ""
    for line in lines:
        giga_line += line

    sub_lines = giga_line.split("don't()")

    sum = 0
    for i in range(len(sub_lines)):
        if i == 0:
            muls = re.findall(r"mul\([0-9]{1,3}\,[0-9]{1,3}\)", sub_lines[i])
        else:
            split = sub_lines[i].split("do()")
            dos = ""
            for j in range(1, len(split)):
                dos += split[j]
            muls = re.findall(r"mul\([0-9]{1,3}\,[0-9]{1,3}\)", dos)

        for mul in muls:
            left_par_idx = mul.find('(')
            comma_idx = mul.find(',')
            right_par_idx = mul.find(')')

            first_value = int(mul[left_par_idx + 1:comma_idx])
            second_value = int(mul[comma_idx + 1:right_par_idx])

            sum += first_value * second_value

    print(sum)


if __name__ == '__main__':
    main()
