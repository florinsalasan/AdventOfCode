import sys


def main():

    if (len(sys.argv) != 2):
        sys.exit('Usage: python calibration.py calibration_document')

    with open(sys.argv[1]) as cali_document:
        lines = cali_document.readlines()

    sum = 0
    for line in lines:
        if line == lines[-1]:
            break
        first_num = None
        last_num = None
        for character in line:
            if character.isdigit():
                if first_num is None:
                    first_num = int(character)
                else:
                    last_num = int(character)
        if last_num is None:
            last_num = first_num
        sum += (first_num * 10) + last_num

    print(sum)
    return sum


if __name__ == '__main__':
    main()
