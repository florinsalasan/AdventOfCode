import sys
import csv


if (len(sys.argv) != 2):
    sys.exit('Usage: python hash.py input.csv')


# Read it in with csv dict reader or something, basically check documentation
values = []
with open(sys.argv[1]) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        for item in row:
            values.append(item)


def hash(str_input):
    # returns a value based on the HASH algorithm described in the
    # specs, add the ASCII value of the char to the starting value,
    # multiply it by 17, take that product and mod by 256 to get the
    # next characters starting value

    starting_value = 0

    for code in str_input.encode('ascii'):
        curr_value = starting_value + code
        curr_value *= 17
        curr_value = curr_value % 256
        starting_value = curr_value

    return starting_value


running_total = 0
for value in values:
    running_total += hash(value)

print(running_total)
