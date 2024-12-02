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

    list3 = []
    for value in list1:
        list3.append(list2.count(value) * value)

    sum = 0
    for value in list3:
        sum += value

    print(sum)


if __name__ == '__main__':
    main()
