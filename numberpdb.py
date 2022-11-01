import argparse

parser = argparse.ArgumentParser(description="Assign numbers to pdb atoms and residues")
parser.add_argument('-i',help="input filename",required=True)
parser.add_argument('-o',help="output filename",required=True)
args = parser.parse_args()

def aligndigit(digit,size):
    if len(str(digit))>=size:return str(digit)
    else:return (" "*(size-len(str(digit))))+str(digit)

def atmline(line):
    if line.startswith("ATOM"):return True
    if line.startswith("HETATM"):return True
    return False

skippedline = 0    
prev_num = -1
res_id = 0
with open(args.o,'w') as outfile:
    with open(args.i,'r') as inpfile:
        for index, line in enumerate(inpfile):
            if not(atmline(line)):skippedline += 1
            try:
                num = int(line[22:26])
                if not(prev_num == num):res_id += 1;prev_num = num
                outfile.write(line[0:6]+aligndigit(index+1-skippedline,5)+line[11:22]+aligndigit(res_id,4)+line[26:])
            except:
                outfile.write(line)
