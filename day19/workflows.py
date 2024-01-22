import sys

if len(sys.argv) != 2:
    sys.exit('usage: python workflows.py input.txt')

# read in the input and place into two different objects of workflows and parts
with open(sys.argv[1]) as input_file:
    all_lines = input_file.readlines()

workflows = all_lines[:all_lines.index('\n')]
parts = all_lines[all_lines.index('\n') + 1:]

# Now make the workflows and parts usable, parts can be changed into dicts, workflows
# can be changed into decision tree maybe.


class decision_node:

    def __init__(self, input_str):
        name = input_str[:input_str.index('{')]
        rules = input_str[input_str.index('{') + 1: input_str.index('}')]
        rules = ''.join(rules)
        rules = rules.split(',')

        classed_rules = []
        for rule_idx, rule in enumerate(rules):
            classed_rules.append((rule_idx, ruleset(rule)))

        self.rules = classed_rules
        self.name = name


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


noded_workflows = []
for workflow in workflows:
    noded_workflows.append(decision_node(workflow))
