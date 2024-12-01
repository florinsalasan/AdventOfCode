import sys

if len(sys.argv) != 2:
    sys.exit('usage: python workflows.py input.txt')

# read in the input and place into two different objects of workflows and parts
with open(sys.argv[1]) as input_file:
    all_lines = input_file.readlines()

workflows = all_lines[:all_lines.index('\n')]
parts = all_lines[all_lines.index('\n') + 1:]

# Now make the workflows and parts usable, parts can be changed into dicts,
# workflows can be changed into decision tree maybe.


class parts_and_values:

    def __init__(self, input_str):
        input_str = input_str[1:-2]
        props = input_str.split(',')
        for prop in props:
            name = prop[0]
            value = prop[2:]
            if name == 'a':
                self.a = int(value)
            elif name == 's':
                self.s = int(value)
            elif name == 'x':
                self.x = int(value)
            elif name == 'm':
                self.m = int(value)

        self.value = self.m + self.x + self.s + self.a

    def __str__(self):
        return ''.join(['m: ', str(self.m), ', x: ', str(self.x), ', s: ', str(self.s), ', a: ', str(self.a)])


class decision_node:

    def __init__(self, input_str):
        name = input_str[:input_str.index('{')]
        rules = input_str[input_str.index('{') + 1: input_str.index('}')]
        rules = ''.join(rules)
        rules = rules.split(',')

        classed_rules = {}
        for rule_idx, rule in enumerate(rules):
            classed_rules[rule_idx] = ruleset(rule)

        self.classed_rules = classed_rules
        self.name = name

    def __str__(self):
        to_return = self.name + '  '
        for rule in self.classed_rules:
            to_return += str(rule[1])
            to_return += ', '
        return to_return


class ruleset:

    def __init__(self, input_str):
        self.input_ = input_str
        if ':' not in input_str:
            self.result = input_str
            self.prop = None
            self.prop_value = None
            self.prop_comp = None
            return
        comp_idx = max(input_str.find('<'), input_str.find('>'))
        colon_idx = input_str.find(':')
        self.result = input_str[colon_idx + 1:]
        self.prop = input_str[:comp_idx]
        self.prop_value = int(input_str[comp_idx + 1:colon_idx])
        self.prop_comp = input_str[comp_idx]

    def __str__(self):
        if self.prop is None:
            return self.result
        return self.prop + self.prop_comp + self.prop_value + self.result

    def passed_rule(self, parts_and_values):
        # check self.prop in parts_and_values.self.prop
        curr_prop = self.prop
        if curr_prop is None:
            return self.result
        curr_comp = self.prop_comp
        # get the value from the passed in part
        if curr_prop == 'x':
            check_against = parts_and_values.x
            if curr_comp == '<':
                return check_against < self.prop_value
            return check_against > self.prop_value
        elif curr_prop == 'm':
            check_against = parts_and_values.m
            if curr_comp == '<':
                return check_against < self.prop_value
            return check_against > self.prop_value
        elif curr_prop == 'a':
            check_against = parts_and_values.a
            if curr_comp == '<':
                return check_against < self.prop_value
            return check_against > self.prop_value
        elif curr_prop == 's':
            check_against = parts_and_values.s
            if curr_comp == '<':
                return check_against < self.prop_value
            return check_against > self.prop_value
        else:
            check_against = 'not found somehow, should never reach here'


noded_workflows = {}
for workflow in workflows:
    curr_workflow = decision_node(workflow)
    noded_workflows[curr_workflow.name] = curr_workflow

classed_parts = []
for part in parts:
    classed_parts.append(parts_and_values(part))

total = 0
cworkflow = noded_workflows['in']
for part in classed_parts:
    # for each part go through the workflow until next reaching a result of 'A'
    # or 'R', if accepted add the value of the part to the total
    passed = False
    count = 0
    # workflows always begins with 'in'
    result = 'not found yet'
    while (not passed and count < len(cworkflow.classed_rules.keys()) and
           result != 'A' and result != 'R'):

        print('part then rule: ')
        print(str(part))
        print(cworkflow.classed_rules[count].input_)
        if cworkflow.classed_rules[count].passed_rule(part):
            # the part passes the rule, get the result from the current rule to
            # update cworkflow, to the next workflow if the result is not 'A' or 'R'
            if cworkflow.classed_rules[count].result == 'A':
                print('inside of accepted')
                print(cworkflow.classed_rules[count].input_)
                total += part.value
                print(total, part.value)
                # break out of the while loop by making count out of bounds
                count += len(cworkflow.classed_rules.keys()) + 1
                # should set result equal to the above conditional in case the special
                # conditions were to ever change but they won't
                result = 'A'
                cworkflow = noded_workflows['in']

            elif cworkflow.classed_rules[count].result == 'R':
                count += len(cworkflow.classed_rules.keys()) + 1
                result = 'R'
                cworkflow = noded_workflows['in']
            else:
                print('passed and going to: ' +
                      cworkflow.classed_rules[count].result)
                cworkflow = noded_workflows[cworkflow.classed_rules[count].result]
                count = -1

        count += 1

print(total)
