import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit('Usage: python3 possible.py puzzle_input')
    with open(sys.argv[1]) as open_file:
        lines = open_file.readlines()

    list1 = []
    list2 = []
    for line in lines:
        first, second = line.split()
        list1.append(int(first))
        list2.append(int(second))

    list1.sort()
    list2.sort()

    sum = 0
    for i in range(len(list1)):
        sum += abs(list1[i] - list2[i])

    print(sum)


if __name__ == '__main__':
    main()
