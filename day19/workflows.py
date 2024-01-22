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
                self.a = value
            elif name == 's':
                self.s = value
            elif name == 'x':
                self.x = value
            elif name == 'm':
                self.m = value


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
        self.prop_value = input_str[comp_idx + 1:colon_idx]
        self.prop_comp = input_str[comp_idx]

    def __str__(self):
        if self.prop is None:
            return self.result
        return self.prop + self.prop_comp + self.prop_value + self.result

    def passed_rule(self, parts_and_values):
        # check self.prop in parts_and_values.self.prop
        curr_prop = self.prop
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
for unclassified_part in classed_parts:
    # go through decsion nodes until result is either 'A' or 'R'
    # if result is 'A' sum the properties in the part and add it to the total
    curr_flow = noded_workflows['in']
    curr_result = 'not found'

    while curr_result != 'A' and curr_result != 'R':
        # check the current part against each rule in the ruleset
        for rule in range(len(curr_flow.classed_rules.keys())):
            curr_flow.classed_rules[rule].passed_rule(unclassified_part)
