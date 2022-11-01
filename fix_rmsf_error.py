import sys
if len(sys.argv)<3:
    print("error in command")
    sys.exit()

filename = sys.argv[1]
outfilename = sys.argv[2]

def align(number,digits):
    number = str(number)
    if len(number)<digits:
        for i in range(digits-len(number)):
            number= " " + number
    return number

counter = 1
with open(outfilename, 'w') as outfile:
    with open(filename,'r') as inpfile:
        for line in inpfile:
            if not(line.startswith("#")) and not(line.startswith("@")):
                line = align(counter,5)+line[5:]
                counter = counter + 1
            outfile.write(line)
