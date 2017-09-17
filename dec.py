import sys
import csv
import glob
import base64
from Crypto.Cipher import ARC4

def all_files(input_path):
    return glob.glob(input_path+"/*/*/*")

def valid_keys(csvdata):
    for row in csvdata:
        if row['alg'] == '4':
            yield row

def main():
    input_path = sys.argv[1]
    input_all_files = all_files(input_path)
    print(input_all_files)
    output_path = sys.argv[2]
    csvfile = sys.argv[3]
    csvdata = []
    keyset = set()
    with open(csvfile, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['key'] not in keyset:
                csvdata.append(row)
                keyset.add(row['key'])
    i = 0
    for key in valid_keys(csvdata):
        key = base64.b64decode(key['key'])
        i += 1
        j = 0
        for filename in input_all_files:
            cipher = ARC4.new(key)
            with open(filename) as f:
                content = f.read()
                result = cipher.decrypt(content)
            with open(output_path+"/" + str(i) + "." + str(j), "w") as f:
                f.write(result)
            j += 1                



if __name__ == "__main__":
    main()