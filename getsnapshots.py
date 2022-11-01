import sys, argparse
parser = argparse.ArgumentParser(description="Gromacs Snapshot Finder")
parser.add_argument('-i',help="Input filename",required=True)
parser.add_argument('-o',help="Output filename",required=True)
parser.add_argument('-s',help="Snapshots to consider",required=True,type=int)
parser.add_argument('-t',help="Timesteps",required=True,type=int)
parser.add_argument('-b',help="Begin from Frame",required=True,type=int)
parser.add_argument('-e',help="End Frame",required=True,type=int)
args = parser.parse_args()

def readrmsd(filename):
    output = []
    with open(filename,'r') as inpfile:
        for line in inpfile:
            if (not(line.startswith("@"))and not(line.startswith("#"))):
                nline = line.strip() # remove white space
                entry = line.split() # split time and distance
                output.append((entry[0],entry[1]))
    return output

def getmaximum(data):
    maxval,count = 0,0
    index = int(float(data[0][0]))
    for entry in data:
        if not(int(float(entry[0]))==index):maxval = max(maxval,count)
        else:count += 1
    maxval = max(maxval,count)
    return maxval

def getsnaps(data,shots,tsteps,t_begin,t_end):
    output = []
    t_data,t_temp,t_segments,t_index = [],[],[i for i in range(t_begin,t_end,tsteps)],0
    t_segments.append(t_end)
    for entry in data:
        if ((int(float(entry[0])) >= t_segments[t_index])):
            if not(int(float(entry[0])) < t_segments[t_index+1]):
                if t_index<len(t_segments)-2:t_index+=1
                if len(t_temp)>0:t_data.append(t_temp)
                t_temp = []
            t_temp.append(entry)
    if len(t_temp)>1:t_data.append(t_temp)
    for segment in t_data:
        curr_data = sorted(segment,key=lambda x :x[1])
        curr_data = curr_data[0:shots]
        curr_data.sort(key=lambda x :x[0])
        output.append(curr_data)
    return output

def printstats(data):
    for entry in data:
        curr = sorted(entry,key=lambda x :x[1])
        print(int(float(entry[0][0])),"ns -",int(float(entry[-1][0])),"ns :",curr[0][1][0:4],"nm -",curr[-1][1][0:4],"nm")

def writesnaps(filename,data):
    with open(filename,'w') as outfile:
        outfile.write("[ frames ]\n")
        counter=0
        for entry in data:
            for subentry in entry:
                outfile.write(subentry[0].replace('.','')[0:4]+" ")
                counter=counter+1
                if counter==15:counter = 0;outfile.write("\n")

try:
    snapshots = int(args.s)
    timestep = int(args.t)
    begin_frame = int(args.b)
    end_frame = int(args.e)
except:
    print("Command Error Found")
    sys.exit()

data = readrmsd(args.i)
maxval = getmaximum(data)
if not((maxval*timestep) > snapshots):
    print("Impossible to get",snapshots,"snapshots from",timestep,"timesteps.\nA maximum of",maxval*timestep,"is possible.")
    sys.exit()
else:
    outdata = getsnaps(data,snapshots,timestep,begin_frame,end_frame)
    printstats(outdata)
    writesnaps(args.o,outdata)
