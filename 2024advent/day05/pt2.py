import sys
import math

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 possible.py puzzle_input')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

rules = []
updates = []
rule_map = set()

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
    rule_map.add((before, after))

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

    if value in values_before.keys():
        for before in befores:
            if before not in values_before[value]:
                return False, "before"

    if value in values_after.keys():
        for after in afters:
            if after not in values_after[value]:
                return False, "after"

    return True, ""


invalid_updates = []
to_sum = []

for update in updates:
    passes = True
    for idx, value in enumerate(update):
        passes, direction = valid_value(update, int(value), idx)
        if not passes:
            invalid_updates.append(update)
            break

total = 0
for update in invalid_updates:
    sub_rules = set()
    for rule in rule_map:
        if rule[0] in update and rule[1] in update:
            sub_rules.add(rule)

    cur_update_numbers = update.copy()
    sorted_update = []

    while len(cur_update_numbers) > 1:
        for num in cur_update_numbers:
            leading_page_update = True
            for rule in sub_rules:
                if num == rule[1]:
                    leading_page_update = False
                    break
            if leading_page_update:
                break

        cur_update_numbers.remove(num)
        sorted_update.append(num)

        # remove the rules containing num
        new_sub_rules = set()
        for rule in sub_rules:
            if rule[0] != num:
                new_sub_rules.add(rule)
            sub_rules = new_sub_rules
    sorted_update.append(cur_update_numbers.pop())

    if sorted_update != cur_update_numbers:
        total += sorted_update[len(sorted_update) // 2]
print(total)
