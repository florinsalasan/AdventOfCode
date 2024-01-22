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
        pieces = list(input_str)
        name = input_str[:input_str.index('{')]
        rules = input_str[input_str.index('{') + 1: input_str.index('}')]
        print(pieces, name, rules)


noded_workflows = []
for workflow in workflows:
    noded_workflows.append(decision_node(workflow))

print(noded_workflows)
