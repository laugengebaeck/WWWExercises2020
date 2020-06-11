import json
import sys
import argparse
import math

get_bin = lambda x: format(x, 'b')

def calc_dict_bits(x):
    if x == 0:
        return 1
    val = math.ceil(math.log2(x))
    return val if val != 0 else 1

def encode(raw_object, minify):
    pattern_table = {}
    for index, token in enumerate(raw_object["dictionary"]):
        pattern_table[token] = index
    pattern = ""
    token_list = []

    for char in raw_object["raw"]:
        if not char in pattern_table:
            sys.exit(25)
        if pattern + char in pattern_table:
            pattern += char
        else:
            pattern_table[pattern + char] = len(pattern_table)
            token_list.append(pattern)
            pattern = char
    if pattern != "":
        token_list.append(pattern)
    
    basic_dictionary = []
    dictionary_bits = 0

    if minify:
        for char in raw_object["dictionary"]:
            if char in token_list:
                basic_dictionary.append(char)
            else:
                for token in pattern_table:
                    if pattern_table[token] > pattern_table[char]:
                        pattern_table[token] -= 1
        dictionary_bits = calc_dict_bits(len(set(token_list)))
    else:
        basic_dictionary = raw_object["dictionary"]
        dictionary_bits = calc_dict_bits(len(pattern_table))

    compressed = ""
    for token in token_list:
        binary = get_bin(pattern_table[token]).rjust(dictionary_bits, '0')
        compressed += binary
    
    compressed_object = {}
    compressed_object["dictionary"] = basic_dictionary
    compressed_object["dictionary_bits"] = dictionary_bits
    compressed_object["compressed"] = compressed
    return compressed_object
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minify", action="store_true")
    args = parser.parse_args()
    data = "".join(sys.stdin.readlines())
    if data == "":
        sys.exit(25)
    raw_object = json.loads(data)
    compressed_object = encode(raw_object, args.minify)
    print(json.dumps(compressed_object), end='')


if __name__ == '__main__':
    main()
