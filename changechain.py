import argparse

parser = argparse.ArgumentParser(description="Assign numbers to pdb atoms and residues")
parser.add_argument('-i',help="input filename",required=True)
parser.add_argument('-b',help="Residue Begin",required=True,type=int)
parser.add_argument('-e',help="Residue End",required=True,type=int)
parser.add_argument('-c',help="chain alphabet",required=True)
parser.add_argument('-o',help="output filename",required=True)
args = parser.parse_args()

def inrange(num,begin,end):
    if ((num>=begin) and (num<=end)):return True
    return False

with open(args.o,'w') as outfile:
    with open(args.i,'r') as inpfile:
        for index, line in enumerate(inpfile):
            try:
                res_num = int(line[22:26])
                if inrange(res_num,args.b,args.e):outfile.write(line[0:21]+args.c[0]+line[22:])
                else:outfile.write(line)
            except:
                outfile.write(line)
