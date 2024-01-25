import sys
import copy

if len(sys.argv) != 2:
    sys.exit('usage: python workflows.py input.txt')

# read in the input and place into two different objects of workflows and parts
with open(sys.argv[1]) as input_file:
    all_lines = input_file.readlines()

workflows = all_lines[:all_lines.index('\n')]

# Take in the workflows and make objects out of them to more easily create the
# ranges that are accepted.

# Ok so need a way to pass on the valid ranges until reaching a condition of 'A'
# or 'R', I think the best way to do that is by implementing the info in the rule
# condition on the boundary set by the rule, and the inverse of that condition to
# pass onto the remaining rules in the workflow. The workflow then generates the
# other workflows that continue doing the same things until all workflows are
# generated. Should the ranges be stored in the rule conditions or on the workflow?
# I think the workflow should hold them, have to deal when the workflow results in
# 'A' to ensurer the inversed rules from earlier also apply to the rule

# define the workflow class and rule_condition class


class rule_condition:

    def __init__(self, input_str, parent_workflow_ranges):
        self.inputted_str = input_str
        self.input_ranges = parent_workflow_ranges
        self.inversed_ranges = copy.deepcopy(self.input_ranges)
        # ranges were set from parents, call _update_ranges to get the new ranges
        # to be used by the workflow class, also to update the self.valid flag
        self.ranges = copy.deepcopy(self.input_ranges)
        self.inversed_valid = True
        self.valid = True
        # the ranges should be fully updated by the time combinations are calculated
        self.combinations = self.get_combinations()
        if ':' not in self.inputted_str:
            self.next_workflow = self.inputted_str
            self.category = None
            self.value = None
            self.comparison = None
            return
        self.category = input_str[0]
        comp_idx = max(input_str.find('<'), input_str.find('>'))
        colon_idx = input_str.find(':')
        self.comparison = input_str[comp_idx]
        self.value = int(input_str[comp_idx + 1:colon_idx])
        self.next_workflow = input_str[colon_idx + 1:]
        self._update_ranges()
        self.get_inverse_range()

    def __str__(self):
        return self.inputted_str

    def _update_ranges(self):
        # The early returns here are rather verbose and not the easiest to follow
        # could make it easier to work with if rewritten, but this should be good
        # enough for this use case

        # using the attributes set from the input string, use them to update
        # the self.ranges value which can then be used by the parent to generate
        # the next workflow or return the number of combinations if reaching an
        # accepted state.
        curr_ranges = self.ranges[self.category]
        # Need different cases based on what the comparison being made is
        # also I need to get a way to apply the inversed restrictions from
        # past rule_conditions. That might be easier to handle in workflow
        # with a method in the rule_condition that handles updating the ranges
        # off of a passed in inverse rule. Explanation is bad but I think I'll
        # be able to understand what I meant later on as well as I do writing it now.
        if self.comparison == '<':
            # restricting the ranges to be less than self.value, so update the ranges
            # if min value is larger than self.value then there are no valid entries
            # ie if the range we were given had 1500 < a < 2500 and the current rule
            # updated it to a < 800, then this path generates 0 valid parts and
            # I should have a way to exit early with a flag or something. Probably
            # not needed for the level of complexity of this input but something to
            # think about implementing if computation ends up taking too long.
            # Basically new max is smaller than existing minimum
            if curr_ranges[0] > self.value:
                self.valid = False
                return curr_ranges
            elif curr_ranges[1] > self.value:
                curr_ranges[1] = self.value
                self.ranges[self.category] = curr_ranges
                return curr_ranges

        # do the same thing as for '<' but now for '>'
        if curr_ranges[1] < self.value:
            # the new range demands values higher than the current max to continue
            # along the workflow order so then no values would be valid anymore
            self.valid = False
            return curr_ranges
        elif curr_ranges[0] < self.value:
            curr_ranges[0] = self.value
        self.ranges[self.category] = curr_ranges
        return curr_ranges

    def get_inverse_range(self):
        # take the comparison type, the value and the category to return a set of
        # ranges to be used in the remaining rules in the workflow
        # Use the input ranges to update the ranges in the opposite way
        curr_ranges = self.inversed_ranges[self.category]
        if self.comparison == '<':
            # if rule is a < 5, inverse is a >= 5 = a > 5 - 1 for integers
            inversed_value = self.value - 1
            # treat the comparison as the opposite so in this case '>'
            if curr_ranges[1] < inversed_value:
                # new rule would be larger than the max, so make it invalid
                self.inversed_valid = False
                return curr_ranges
            elif curr_ranges[0] < inversed_value:
                curr_ranges[0] = inversed_value
                self.inversed_ranges[self.category] = curr_ranges
                return curr_ranges

        # now the comparison is '>' if we're here so act as if it is '<'
        # inversed value should be value + 1, a > 5 -> a <= 5 -> a < 5 + 1
        inversed_value = self.value + 1
        if curr_ranges[0] > inversed_value:
            # the minimum value is larger than the new max so make it invalid
            self.inversed_valid = False
            return curr_ranges
        elif curr_ranges[1] > inversed_value:
            curr_ranges[1] = inversed_value
            self.inversed_ranges[self.category] = curr_ranges
            return curr_ranges

    def get_combinations(self):
        if not self.valid:
            return 0
        # initialize with 1 to multiply all together
        running_total = 1
        for key in self.ranges:
            curr_min, curr_max = self.ranges[key]
            running_total *= (curr_max - curr_min - 1)

        return running_total


class workflow:

    def __init__(self, input_str, ranges):
        # given a string containing all of the information about a workflow,
        # generate the object.

        # have the input_str available as an attribute to check that the other
        # properties have been set correctly from the string slicing.
        self.inputted_str = input_str
        end_name_idx = self.inputted_str.index('{')
        close_rules_idx = self.inputted_str.index('}')
        self.name = self.inputted_str[:end_name_idx]
        rules = self.inputted_str[end_name_idx + 1: close_rules_idx].split(',')
        classed_rules = {}
        self.ranges = ranges
        for i, rule in enumerate(rules):
            if i == 0:
                classed_rules[i] = rule_condition(rule, self.ranges)
            else:
                classed_rules[i] = rule_condition(rule,
                                                  classed_rules[i - 1].inversed_ranges)
        # Once the rules in the workflow have been generated, create the workflows
        # from them passing in the inversed ranges when necessary and the updated
        # range if not needed.
        # Ok quick break. Ranges are passed into the workflow init method, then
        # the rule_condition runs update and inversed range methods to generate 2
        # new ranges. The updated range needs to be used to generate the workflow
        # for the current ruleset, the inversed range should instead be used to
        # generate the initial range for the rule_condition init method.
        next_workflows = []
        for key in classed_rules.keys():
            # use a dict that has keys that are the name of the workflow, and
            # values that are the string from the input file
            # need to pass in input str and the proper range from ruleset
            new_name = classed_rules[key].next_workflow
            if new_name == 'R':
                continue
            elif new_name == 'A':
                # get combination by multiplying each of the range counts together
                # need to get the range from the rule condition object
                combinations = classed_rules[key].get_combinations()
                print(combinations)
                continue
            new_input_str = workflow_name_to_str[new_name]
            new_workflow = workflow(new_input_str, classed_rules[key].ranges)
            next_workflows.append(new_workflow)

        self.next_workflows = next_workflows

    def __str__(self):
        return self.inputted_str


# Creating all of the workflows in a loop doesn't really work with the way I've set
# it up since the root node will always be the 'in' workflow, so need to begin with
# that and then generate it from there.
starter_ranges = {
    'x': [1, 4000],
    'm': [1, 4000],
    'a': [1, 4000],
    's': [1, 4000],
}


workflow_name_to_str = {}
for _workflow in workflows:
    end_of_name_idx = _workflow.find('{')
    name = _workflow[:end_of_name_idx]

    workflow_name_to_str[name] = _workflow

for _workflow in workflows:
    if _workflow[:2] == 'in':
        root = workflow(_workflow, starter_ranges)
