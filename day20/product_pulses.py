import sys

if len(sys.argv) != 2:
    sys.exit('usage: python product_pulses.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()


class broadcast:

    def __init__(self, input_str):
        self.input_str = input_str
        print('broadcasted')
        items = input_str.split(' ')
        self.title = items[0]
        separator = items.index('->')
        self.destinations = items[separator + 1:]
        print(self.title, self.destinations)

    def _send(self):
        # Only sends when receiving a signal from the button press, button press
        # always sends a single low pulse to the broadcast module.
        signals = []
        for destination in self.destinations:
            signals.append(('low', destination))
        return signals


class conjunction:

    def __init__(self, input_str):
        self.input_str = input_str
        print('conjucted')
        items = input_str.split(' ')
        self.title = items[0][1:]
        separator = items.index('->')
        self.destinations = items[separator + 1:]
        print(self.title, self.destinations)
        self.received_signals = {}
        self.all_high = False
        self.input_modules = []

    def receive_signal(self, input_signal):
        # signals sent and received are all going to be tuples of len 2, first
        # item is signal type ie high or low, 2nd item is the module that sent
        # it, afterwards need to check what signal to send
        self.received_signals[input_signal[1]] = input_signal[0]
        for key in self.received_signals:
            if self.received_signals[key] == 'low':
                self.all_high = False
                return
        # if it reaches here then all of the input signals are high
        self.all_high = True
        return

    def send_signal(self):
        signals = []
        for destination in self.destinations:
            if self.all_high:
                signals.append(('low', destination))
            else:
                signals.append(('high', destination))
        return signals

    def add_input_module(self, title):
        self.input_modules.append(title)
        self.received_signals[title] = 'low'
        self.all_high = False


class flip_flop:

    def __init__(self, input_str):
        self.input_str = input_str
        print('flip flopped')
        items = input_str.split(' ')
        self.title = items[0][1:]
        separator = items.index('->')
        self.destinations = items[separator + 1:]
        print(self.title, self.destinations)


class generic_module:

    def __init__(self, input_str):
        items = input_str.split(' ')
        newline_removed = items[-1][0:-1]
        items[-1] = newline_removed
        prefix = items[0][0]
        self.input_str = ' '.join(items)
        self.creation = None
        if prefix == '%':
            self.creation = flip_flop(self.input_str)
        elif prefix == '&':
            self.creation = conjunction(self.input_str)
        elif items[0] == 'broadcaster':
            self.creation = broadcast(self.input_str)


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
    modules[new_module.creation.title] = new_module.creation

for key in modules.keys():
    print(key, modules[key])
