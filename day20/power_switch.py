import sys

if len(sys.argv) != 2:
    sys.exit('usage: python product_pulses.py input.txt')

with open(sys.argv[1]) as input_file:
    lines = input_file.readlines()


class broadcast:

    def __init__(self, input_str):
        self.input_str = input_str
        items = input_str.split(' ')
        self.title = items[0]
        separator = items.index('->')
        self.destinations = items[separator + 1:]
        self.inputs = []

    def send_signal(self):
        # Only sends when receiving a signal from the button press, button press
        # always sends a single low pulse to the broadcast module.
        signals = []
        for destination in self.destinations:
            signals.append(('low', destination, 'broadcaster'))
        return signals

    def receive_signal(self, input_signal):
        return

    def receive_input(self, inputted_input):
        self.inputs.append(inputted_input)

    def __str__(self):
        return 'broadcast: ' + self.input_str


class conjunction:

    def __init__(self, input_str):
        self.input_str = input_str
        items = input_str.split(' ')
        self.title = items[0][1:]
        separator = items.index('->')
        self.destinations = items[separator + 1:]
        self.all_high = False
        self.input_modules = dict()

    def receive_signal(self, input_signal):
        # signals sent and received are all going to be tuples of len 2, first
        # item is signal type ie high or low, 2nd item is the module that sent
        # it, afterwards need to check what signal to send
        self.input_modules[input_signal[-1]] = input_signal[0]
        for key in self.input_modules.keys():
            if self.input_modules[key] == 'low':
                self.all_high = False
                return
        # if it reaches here then all of the input signals are high
        self.all_high = True
        return

    def send_signal(self):
        signals = []
        for destination in self.destinations:
            if self.all_high:
                signals.append(('low', destination, self.title))
            else:
                signals.append(('high', destination, self.title))
        return signals

    def __str__(self):
        return 'conjunction: ' + self.input_str


class flip_flop:

    def __init__(self, input_str):
        self.input_str = input_str
        items = input_str.split(' ')
        self.title = items[0][1:]
        separator = items.index('->')
        self.destinations = items[separator + 1:]
        self.on = False
        self.last_received = None

    def receive_signal(self, signal):
        if signal[0] == 'low':
            self.on = not self.on
        self.last_received = signal[0]

    def send_signal(self):
        # only ever call this after receive_signal so that self.on is properly set
        if self.last_received == 'high':
            return
        signals = []
        if self.on:
            signal_strength = 'high'
        else:
            signal_strength = 'low'
        for dest in self.destinations:
            signals.append((signal_strength, dest, self.title))
        return signals

    def __str__(self):
        return 'flip flop: ' + self.input_str


class power_switch:
    def __init__(self, input_str):
        self.input_str = input_str
        self.one_low = False

    def receive_signal(self, signal):
        print(signal[0])
        if signal[0] == 'low':
            self.one_low = True
    
    def send_signal(self):
        return

    def check_power(self):
        return self.one_low



class untyped:
    def __init__(self, input_str):
        self.input_str = input_str
        self.destinations = None

    def receive_signal(self, signal):
        # do nothing since this is just an endpoint module
        return

    def send_signal(self):
        # do nothing since this is just an endpoint module
        return


class generic_module:

    def __init__(self, input_str):
        no_cleaning = input_str
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
        elif no_cleaning == 'rx':
            self.creation = power_switch(self.input_str)
        else:
            self.creation = untyped(self.input_str) 

    def __str__(self):
        return str(self.creation)


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
    modules[new_module.creation.title] = new_module.creation
# once the modules are created and stored in the dict, go through all of them 
# again and check if any of their destinations is a conjunction, if so add, 
# the current module as the destinations input
endpoint_modules = {}
for key in modules.keys():
    curr_module = modules[key]
    if curr_module.destinations:
        for dest in curr_module.destinations:
            if dest[-1] == ',':
                dest = dest[:-1]
            if dest not in modules.keys():
                endpoint_modules[dest] = generic_module(dest).creation
                continue
            dest_module = modules[dest]
            if type(dest_module) is conjunction:
                dest_module.input_modules[key] = 'low'

for key in endpoint_modules.keys():
    modules[key] = endpoint_modules[key]

# work backwords from the rx end module to the modules feeding in, honestly
# I don't get how this will ever proc since this seemingly loops the same 3 states,
# and there would be no way for that to ever change unless I'm being giga dumb
# Add in a prop for all classes of their inputs, then have a method to add 
# each one, going to do this reverse order somehow someway, ie instead of pressing
# the button going to 'send' a signal from 'rx' to it's inputs and so on
