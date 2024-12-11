import sys
import operator
import itertools
import functools

if (len(sys.argv) != 2):
    sys.exit('Usage: python3 pt1.py puzzle_input.txt')
with open(sys.argv[1]) as open_file:
    lines = open_file.readlines()

targets_and_elements = {}
for line in lines:
    split1 = line.split(":")
    target = int(split1[0])
    split2 = split1[1][1:].split(" ")
    int_elements = [int(element) for element in split2]
    targets_and_elements[target] = int_elements


@functools.lru_cache
def get_operator_permutations(ops, num_parameters):
    op_permutations = list(itertools.product(ops, repeat=num_parameters-1))
    return op_permutations


def apply_operator(nums, op):
    match op:
        case "+":
            return operator.add(nums[0], nums[1])
        case "*":
            return operator.mul(nums[0], nums[1])
        case _:
            print("Using invalid operator")


def solve(data, ops):
    total = 0
    for key in data.keys():
        nums = data[key]
        print("Key being looked at: ", key, " elements: ", nums)
        op_perms = get_operator_permutations(ops, len(nums))

        for idx, op_perm in enumerate(op_perms):
            # apply operator as we go through the elements
            res = nums[0]
            for i, op in enumerate(op_perm):
                res = apply_operator((res, nums[i+1]), op)

            if res == key:
                total += key
                break

    return total


print(solve(targets_and_elements, "+*"))
