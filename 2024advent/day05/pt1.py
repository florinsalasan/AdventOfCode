import sys
import math

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 possible.py puzzle_input')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

rules = []
updates = []

gap = False
for line in lines:
    if line == "\n":
        gap = True
        continue
    if not gap:
        rules.append(line)
    else:
        line_list = line.split(',')
        inted_list = []
        for item in line_list:
            inted_list.append(int(item))
        updates.append(inted_list)

values_before = {}
values_after = {}

for rule in rules:
    before, after = rule.split('|')
    before, after = int(before), int(after)
    if after in values_before.keys():
        values_before[after].append(before)
    else:
        values_before[after] = [before]
    if before in values_after.keys():
        values_after[before].append(after)
    else:
        values_after[before] = [after]


def valid_value(update, value, idx):

    befores = update[:idx]
    if idx == len(update) - 1:
        afters = []
    else:
        afters = update[idx + 1:]

    # print("update list: ", update, " and before and after for ", value,
    # " ", befores, afters)
    if value in values_before.keys():
        # print("value: ", value, " values_before: ",  values_before[value])
        for before in befores:
            # print(before in values_before[value])
            if before not in values_before[value]:
                return False

    if value in values_after.keys():
        # print("value: ", value, " values_after: ",  values_after[value])
        for after in afters:
            if after not in values_after[value]:
                return False

    return True


valid_updates = []
to_sum = []

for update in updates:
    passes = True
    # print("update passed into valid_values: ", update)
    for idx, value in enumerate(update):
        passes = valid_value(update, int(value), idx)
        if not passes:
            break
    if passes:
        valid_updates.append(update)
        to_sum.append(update[math.floor(len(update)/2)])

# print("'valid_updates allegedly': ", valid_updates)
# print("middle values of those valid_updates:", to_sum)
print("sum of the middle_values: ", sum(to_sum))
# print("values_before: ", values_before)
# print("values_after: ", values_after)
