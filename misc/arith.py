import json
import argparse
import sys

def encode(string, lower_value=0.0, higher_value=1.0):
    probs = {}
    accprobs = {}
    for char in string:
        if char in probs:
            probs[char] += 1.0
        else:
            probs[char] = 1.0
    for key in probs:
        probs[key] /= float(len(string))
    probs = dict(sorted(probs.items()))
    lowerbefore = lower_value
    for key in probs:
        accprobs[key] = (lowerbefore, lowerbefore + probs[key])
        lowerbefore = lowerbefore + probs[key]
    for _, char in enumerate(string):
        for key in accprobs:
            new_lower_value = lower_value + (higher_value - lower_value) * accprobs[key][0]
            new_higher_value = lower_value + (higher_value - lower_value) * accprobs[key][1]
            if key == char:
                lower_value = new_lower_value
                higher_value = new_higher_value
                break
    output = {}
    output["probabilities"] = probs
    output["data"] = lower_value
    output["length"] = len(string)
    output["interval"] = [0.0, 1.0]
    return output

# encoded_object should be an object, not the JSON string
def decode(encoded_object) -> str:
    accprobs = {}
    probs = encoded_object["probabilities"]
    decoded_string = ""
    lowerbefore = encoded_object["interval"][0]
    lower_value = encoded_object["interval"][0]
    higher_value = encoded_object["interval"][1]
    diff = higher_value - lower_value
    for key in probs:
        accprobs[key] = (lowerbefore, (lowerbefore + probs[key]) * diff)
        lowerbefore = (lowerbefore + probs[key]) * diff
    for _ in range(encoded_object["length"]):
        for key in accprobs:
            new_lower_value = lower_value + (higher_value - lower_value) * accprobs[key][0]
            new_higher_value = lower_value + (higher_value - lower_value) * accprobs[key][1]
            if encoded_object["data"] >= new_lower_value and encoded_object["data"] < new_higher_value:
                decoded_string += key
                lower_value = new_lower_value
                higher_value = new_higher_value
                break
    return decoded_string
    # implement decoding here
    # should return encoded string

def main():
    # parse arguments here, allow switching between encoding (argument --action encode) and decoding (argument --action decode) while defaulting to encoding. Read data from stdin.
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", action="store", default="encode")
    args = parser.parse_args()
    data = "".join(sys.stdin.readlines())
    if data == "":
        sys.exit(42)
    if args.action == "decode":
        decoded = decode(json.loads(data))
        print(decoded, end='')
    elif args.action == "encode":
        encoded = encode(data)
        print(json.dumps(encoded), end='')
    else:
        sys.exit(21)
    # You should print the encoded (JSON dump) to stdout as well as the decoded strings. Watch out for final newlines.

# To be able to run this script directly from command line (locally)
if __name__ == '__main__':
    main()
