import sys

if len(sys.argv) != 2:
    sys.exit('usage: python product_pulses.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()


class flip_flop:

    def __init__(self, input_str):
        self.input_str = input_str
        print('flip flopped')


class generic_module:

    def __init__(self, input_str):
        self.input_str = input_str
        items = input_str.split(' ')
        newline_removed = items[-1][0:-1]
        items[-1] = newline_removed
        prefix = items[0][0]
        self.creation = None
        if prefix == '%':
            self.creation = flip_flop(input_str)


modules = {}
# Keys in modules should be the module name ignoring type since that will be
# defined in the class it's placed into
for line in lines:
    # format the lines in here. Should create multiple classes to properly handle
    # the differing roles they all have instead of a spaghetti mess of scripting
    # and checking the type of module each time.
    # generic_module will be a factory class that places the line in the proper
    # module subclass
    new_module = generic_module(line)
    print('new module: ' + line)
    print(type(new_module))
    print(type(new_module.creation))
