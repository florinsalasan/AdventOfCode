import sys

if len(sys.argv) != 2:
    sys.exit('usage: python workflows.py input.txt')

# read in the input and place into two different objects of workflows and parts
with open(sys.argv[1]) as input_file:
    all_lines = input_file.readlines()

workflows = all_lines[:all_lines.index('\n')]

# Take in the workflows and make objects out of them to more easily create the
# ranges that are accepted.

# define the workflow class


class workflow:

    def __init__(self, input_str):
        # given a string containing all of the information about a workflow,
        # generate the object.
        self.inputted_str = input_str
        print(self.inputted_str)
        end_name_idx = self.inputted_str.index('{')
        close_rules_idx = self.inputted_str.index('}')
        self.name = self.inputted_str[:end_name_idx]
        rules = self.inputted_str[end_name_idx + 1: close_rules_idx].split(',')
        print('rules: ' + str(rules))
        print(self.name)
        print('\n')


for workflow_ in workflows:
    curr_workflow = workflow(workflow_)
