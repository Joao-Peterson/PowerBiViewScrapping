#!/usr/bin/python 

import sys
import csv
import json

# Converts the JSON output of a PowerBI query to a CSV file
def extract(input_file, output_file):
    input_json = read_json(input_file)
    data = input_json["results"][0]["result"]["data"]
    ph = data["dsr"]["DS"][0]["PH"]
    valueDicts = data["dsr"]["DS"][0].get("ValueDicts", {})

    # matrix
    institutions = [["Instituição", "Instituição Dependente"]]

    # all data
    for matrices in ph:
        # data matrices
        for dataMatrix in matrices.values():
            valueDictName = "D0"

            # parent company
            for inst in dataMatrix:
                instName = inst.get("G0", None)
                if instName != None:
                    print(instName)

                    # refs
                    for dms in inst["M"]:
                        for props in dms.values():
                            for ref in props:

                                # value dict ref
                                s = ref.get("S", None)
                                if s != None:
                                    n = s[0].get("N", None)
                                    dn = s[0].get("DN", None)
                                    if n != None and n == "G1" and dn != None:
                                        valueDictName = dn
                                        # print(f"New dict!: {valueDictName}")

                                # column
                                column = ref.get("C", None)
                                if column != None:

                                    # ref value
                                    if isinstance(column[0], int):
                                        pos = int(column[0])
                                        instChild = valueDicts[valueDictName][pos]
                                        # print("\t" + instChild)
                                        institutions.append([instName, instChild])
                                    # literal
                                    else:
                                        institutions.append([instName, column[0]])
                                        

    write_csv(output_file, institutions)

def read_json(file_name):
    with open(file_name) as json_config_file:
        return json.load(json_config_file)

def write_csv(output_file, matrix):
    with open(output_file, "w") as csvfile:
        wrt = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)

        for row in matrix:
            wrt.writerow(row)

def main():
    if len(sys.argv) == 3:
        extract(sys.argv[1], sys.argv[2])
    else:
        sys.exit("Usage: python3 " + sys.argv[0] + " input_file output_file", file=sys.stderr)

if __name__ == "__main__":
    main()