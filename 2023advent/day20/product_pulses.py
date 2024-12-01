import sys
import math

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

    def send_signal(self):
        # Only sends when receiving a signal from the button press, button press
        # always sends a single low pulse to the broadcast module.
        signals = []
        for destination in self.destinations:
            signals.append(('low', destination, 'broadcaster'))
        return signals

    def receive_signal(self, input_signal):
        print('broadcast received a signal')

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
                print('received low signal')
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
                endpoint_modules[dest] = untyped(dest)
                continue
            dest_module = modules[dest]
            if type(dest_module) is conjunction:
                dest_module.input_modules[key] = 'low'

for key in endpoint_modules.keys():
    modules[key] = endpoint_modules[key]

def button_press(defined_modules, button_press_count, last_memo={}):
    # start count at 1 since there is a button pushed
    memo = last_memo
    reverse_lookup = {}
    low_count = 0
    high_count = 0
    count = 0
    '''for key in defined_modules:
        if type(defined_modules[key]) is conjunction:
            print(defined_modules[key].input_modules)'''
    # q should contain the signals being sent to the different modules that 
    # are in the defined_modules
    while count < button_press_count:
        # each loop acts as a button press
        low_count += 1
        q = []
        input_history = []
        q.append(('low', 'broadcaster', 'button'))
        while q:
            curr_signal = q.pop(0)
            # actually ordered like in the example:
            to_print = (curr_signal[-1], curr_signal[0], curr_signal[1])
            input_history.append(to_print)
            affected_module_title = curr_signal[1]
            if affected_module_title[-1] == ',':
                affected_module_title = affected_module_title[:-1]
            curr_module = defined_modules[affected_module_title]
            curr_module.receive_signal(curr_signal)
            append_these = curr_module.send_signal()
            if append_these:
                for item in append_these:
                    if item[0] == 'low':
                        low_count += 1
                    else:
                        high_count += 1
                    q.append(item)

        # memo the input history as a tuple
        final_inputs = tuple(input_history)
        reverse_lookup[count] = final_inputs
        #if final_inputs in memo.keys():
            # get the result which is the count then do math to get count similar
            # to method used in the tilting stones puzzle.
            # assume loop always begins at 0, adjust multipliction by the remainder of the loop
            #len_loop = count + 1
            #remainder = button_press_count % len_loop
            # from remainder grab the reverse lookup to then get the count of low and high 
            # signals that were sent as extra values to add
            #if remainder == 0:
                #extra_lows, extra_highs = 0, 0
            #else:
                #extra_lows_and_highs = memo[reverse_lookup[remainder - 1]]
                #_, extra_lows, extra_highs = extra_lows_and_highs
            #all_lows = low_count * math.floor(button_press_count / len_loop) + extra_lows
            #all_highs = high_count * math.floor(button_press_count / len_loop) + extra_highs
            # something in this is goofed and I'm too tired to debug it now, the two test inputs 
            # work too which makes it extra annoying
            #return (all_lows * all_highs)

            # return (low_count * (button_press_count / (count + 1)) * (high_count * (button_press_count / (count + 1))))
        memo[final_inputs] = (count, low_count, high_count)
        #for sent_signal in input_history:
            #print(sent_signal)
        count += 1
    return (low_count * high_count)


print(button_press(modules, 1000))
