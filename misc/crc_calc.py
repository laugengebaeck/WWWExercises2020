import argparse
import sys
from bitstring import BitArray

def calc_crc(inputstring, poly):
    left_index = 0
    right_index = len(poly)
    zeroes = '0'*(len(poly)-1)
    inputstring.append(BitArray(bin=zeroes))
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
    start_pos = 0
    while start_pos < len(xored) and xored[start_pos] == 0:
        start_pos += 1
    xored = xored[start_pos:]
    xored.append(BitArray(bin='0'*(len(poly)-1-len(xored))))
    return xored

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('poly')
    parser.add_argument("--transmit-data", action='store_true')
    parser.add_argument("--pad-proof", action='store_true')
    args = parser.parse_args()
    try:
        poly = BitArray(bin=args.poly)
        inputstring = BitArray(bin=args.input)
    except ValueError:
        sys.exit(2)
    if poly[0] == 0:
        sys.exit(2)
    crc = calc_crc(inputstring, poly)
    if args.pad_proof:
        crc.invert()
    if args.transmit_data:
        print(args.input + crc.bin, end='')
    else:
        print(crc.bin, end='')


if __name__ == '__main__':
    main()
