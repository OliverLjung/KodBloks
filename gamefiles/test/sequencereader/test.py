import os
from getCodes import getCodes


expectedResult = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
    "8": [],
    "9": [],
    "10": [],
    "11": [],
    "12": [],
    "13": [],
    "14": [],
    "15": [],
    "16": [],
    "17": [],
    "18": [],
    "19": [],
    "20": []
}

stats = 0

for nr in range(1,21):
    filename = f"files/fil{nr}.jpg"
    os.rename(filename,"fil")
    thisExpected = expectedResult[f"{nr}"]
    # Run test
    thisResult = getCodes()

    if thisExpected == thisResult:
        r = "Passed"
        stats += 1
    else:
        r = "Failed"
    
    print(f"Test{nr}: {}")
    # 
    os.rename("bild.jpg", bildname)

print(f"\nProcentage passed: {stats/20 * 100}%")