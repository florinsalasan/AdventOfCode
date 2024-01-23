import sys

if len(sys.argv) != 2:
    sys.exit('usage: python workflows.py input.txt')

# read in the input and place into two different objects of workflows and parts
with open(sys.argv[1]) as input_file:
    all_lines = input_file.readlines()

workflows = all_lines[:all_lines.index('\n')]
parts = all_lines[all_lines.index('\n') + 1:]

# parts can have values between 1 and 4000 inclusive for each property.
# Find the number of distinct ratings that are accepted by the workflows.

# take the different paths to reaching an 'A' result, keeping track of the
# restrictions on part props then find the number of combinations left at
# each 'A' leaf using those restrictions. For example:
# in -> px -> 'A' using s < 1351 and m > 2090 to reach A. from there we get
# 4000 * 4000 * 1350 * (4000 - 2090). Do this for all paths. Now this is fairly
# trivial to do as a human looking for paths to an A, I think it's harder for
# me to think of a way to do this programmatically. I'm thinking build an
# actual tree from the workflows, then travel to each leaf tracking the
# restrictions, finally check the leaf if it's an A then 'count' the number of
# distinct comnbinations.

# List of combos for sanity check before writing out the algo;
# in - > px - > A = 41256000000000
# in -> px -> qkq -> A = 1350 * 2005 * 1415 * 4000 = 15320205000000
# in -> px -> qkq -> crn -> A = 1350 * 2005 * (4000 - 2662) * 4000 = 14486526000000
# in -> px -> qkq -> crn -> R = 0
# From this line below, order should be x, m, a, s
# in -> px -> rfg -> A = (0 < x <= 2440) * (0 < m < 2091) * (2006 < a < 4001)
#    * (537 <= s < 1351) = 2440 * 2090 * (4000 - 2005) * (1351 - 537) = 828139428000
# in -> px -> rfg -> gd -> R in any case so 0
# in -> px -> rfg -> R in any other case so 0, px is all accounted for, so in -> qqz
# in -> qqz -> qs -> A = s > 3448 so 4000^3 * (4000 - 3448) = 35328000000000
# in -> qqz -> qs -> lnx -> A no matter what, so 1351 <= s <= 2770
# = 4000^3 * (2770 - 1351) = 90816000000000
# By this path I've already exceeded the number of distinct combinations by ~30
# trillion so something is clearly off in the way I'm counting ranges
# remaining. I took a peak at David Brownman's solution again to see if I'm at
# least on the right track and I seemingly am. So maybe I'll just work on the
# actual code instead of trying to manually track the solutions.


# Let's build the decision tree.
# First take the class for workflows from pt1
# might be easier to rewrite from scratch. will rewrite from scratch

class decision_tree:
    # given a root node, build out tree from here

    def __init__(self, root_node):
        # for each rule in the root node need to create a new node, for each node
        # after the first treat the previous rules as failed and add them as inversed

        # TODO: figure out updating ranges of different props as we move through the
        # tree. should be handled on the decision nodes themselves I think.
        print(str(root_node))


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
        self.inversed_comp, self.inversed_value = self.inverse()

    def __str__(self):
        if self.prop is None:
            return self.result
        return self.prop + self.prop_comp + str(self.prop_value) + self.result

    def inverse(self):
        if self.prop_comp == '<':
            inversed_comp = '>'
            inversed_value = self.prop_value - 1
            return inversed_comp, inversed_value
        return '<', self.prop_value + 1


class decision_node:

    def __init__(self, input_str, ranges):
        name = input_str[:input_str.index('{')]
        rules = input_str[input_str.index('{') + 1: input_str.index('}')]
        rules = ''.join(rules)
        rules = rules.split(',')

        classed_rules = {}
        for rule_idx, rule in enumerate(rules):
            classed_rules[rule_idx] = ruleset(rule)

        self.classed_rules = classed_rules
        self.name = name

        self.ranges = ranges
        self.ltx = ranges['x'][0]
        self.gtx = ranges['x'][1]
        self.ltm = ranges['m'][0]
        self.gtm = ranges['m'][1]
        self.lta = ranges['a'][0]
        self.gta = ranges['a'][1]
        self.lts = ranges['s'][0]
        self.gts = ranges['s'][1]

    def __str__(self):
        to_return = self.name + ': \n'
        for rule in self.classed_rules.keys():
            to_return += str(self.classed_rules[rule])
            to_return += ', \n'
            ranges_strd = str(self.ranges)
            to_return += ranges_strd + '  \n '
        return to_return

    def update_ranges(self, ranges: dict, rule: ruleset):
        # take the rule, update the range to create the next step in the path
        range_key = rule.prop
        comp = rule.prop_comp
        value = rule.prop_value
        new_node_name = rule.result

    def calc_ranges(self):
        # given all of the ranges on the decision node, return the number of
        # combinations possible at this node.
        return ((self.gtx - self.ltx) * (self.gtm - self.ltm) *
                (self.gta - self.lta) * (self.gts - self.lts))


# Have the parsing set up from part 1, want a way for the decision node to have valid
# inputs stored as a property, then a function that updates the range based on the
# ruleset we follow to the nex decision node.

default_ranges = {
    'x': [1, 4000],
    'm': [1, 4000],
    'a': [1, 4000],
    's': [1, 4000]
}

for workflow in workflows:
    if 'in' in workflow:
        root = decision_node(workflow, default_ranges)

decision_tree(root)
