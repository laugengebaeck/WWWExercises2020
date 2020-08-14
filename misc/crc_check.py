import argparse
import sys
from bitstring import BitArray

def check_crc(inputstring, poly):
    left_index = 0
    right_index = len(poly)
    first_operand = inputstring[left_index:right_index]
    xored = BitArray(bin='0000')
    while right_index <= len(inputstring):
        xored = first_operand ^ poly
        new_left = 0
        while new_left < len(xored) and xored[new_left] == 0:
            new_left += 1
        needed_bits = len(poly) - (len(xored) - new_left)
        if right_index + needed_bits > len(inputstring):
            break
        xored = xored[new_left:len(xored)]
        xored.append(inputstring[right_index:right_index + needed_bits])
        first_operand = xored
        right_index = right_index + needed_bits
        left_index = right_index - len(poly)
    return xored.all(0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('poly')
    args = parser.parse_args()
    try:
        poly = BitArray(bin=args.poly)
        inputstring = BitArray(bin=args.input)
    except ValueError:
        sys.exit(2)
    if poly[0] == 0:
        sys.exit(2)
    if not check_crc(inputstring, poly):
        sys.exit(25)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
