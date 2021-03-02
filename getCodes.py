# imports
import re
import os.path
import time

#
def main():
    codes = getCodes()
    print(codes)

def getCodes():
    while not os.path.exists("fil"):
        time.sleep(1)
    fil = open("fil", "r")
    rawRawText = fil.read()
    rawText = rawRawText.split("\n")
    codes = []
    for line in rawText[4:-2]:
        codes.append(line[20:])
    return codes



if __name__ == "__main__":
    main()