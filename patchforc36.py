import argparse

parser = argparse.ArgumentParser(description="Prepare Discovery studio CHARMM36 for Gromacs CHARMM36")
parser.add_argument('-i',help="input filename",required=True)
parser.add_argument('-o',help="output filename",required=True)
parser.add_argument('-r',help="Flag to remove protonated GLU/ASP H", action='store_true')
args = parser.parse_args()


"""
ARG HH11 HH12 HH21 HH22
ASN HD21 HD22
CYS HG1 --CYN
GLN HE21 HE22
HSE HE2
HSD HD1
ILE HG21 HG22 HG23 HG11 HG12
LEU HD11 HD12 HD13 HD21 HD22 HD23
SER HG -> HG1
THR HG21 HG22 HG23
VAL HG11 HG12 HG13 HG21 HG22 HG23
"""


def proc_NCterm(data):
    ps = [["HT1"," HN"],["HT2"," HN"],["HT3"," HN"],["1OCT","   O"],["2OCT","   O"]]
    for index in range(0,len(data)):
        for p in ps:
            data[index] = data[index].replace(p[0],p[1])
    return data

def ishse(data):
    for line in data:
        if "HE2" in line.upper():return True
    return False

def defaultaa(data):
    return data

def proc_default(data,dicti,name=""):
    for index in range(0,len(data)):
        if not(name==""):data[index] = data[index].replace(data[index][17:20],name.upper())
        for p in dicti:
            data[index] = data[index].replace(p[0],p[1])
    return data

def proc_val(data): #16
    ps = [["1HG1","HG11"],["2HG1","HG12"],["3HG1","HG13"],["1HG2","HG21"],["2HG2","HG22"],["3HG2","HG23"]]
    return proc_default(data,ps,"")

def proc_thr(data): #14
    ps = [["1HG2","HG21"],["2HG2","HG22"],["3HG2","HG23"]]
    return proc_default(data,ps,"")

def proc_ser(data): #11
    ps = [[" HG","HG1"]]
    return proc_default(data,ps,"")

def proc_lys(data):#21:lsn ,22:lys
    if len(data)>21:
        return data
    else:
        ps = [["",""]]
        return proc_default(data,ps,"LSN")

def proc_leu(data): #19
    ps = [["1HD1","HD11"],["2HD1","HD12"],["3HD1","HD13"],["1HD2","HD21"],["2HD2","HD22"],["3HD2","HD23"]]
    return proc_default(data,ps,"")

def proc_ile(data): #19
    ps = [["1HG2","HG21"],["2HG2","HG22"],["3HG2","HG23"],["1HG1","HG11"],["2HG1","HG12"]]
    return proc_default(data,ps,"")

def proc_his(data): #18:hsp ,17:hse, 17:hsd
    if len(data)>17:
        ps = [["",""]]
        return proc_default(data,ps,"HSP")
    else:
        if ishse(data):
            ps = [["",""]]
            return proc_default(data,ps,"HSE")
        else:
            ps = [["",""]]
            return proc_default(data,ps,"HSD")
        

def proc_gln(data): #17
    ps = [["1HE2","HE21"],["2HE2","HE22"]]
    return proc_default(data,ps,"")

def proc_glu(data): #16:glupp ,15:glu
    if len(data)>15:
        if args.r:
            t_data = []
            for i in data:
                if not('HE2' in i):t_data.append(i)
            return t_data
        else: 
            ps = [["",""]]
            return proc_default(data,ps,"GLH")
    return data

def proc_cys(data): #11:cys ,10:cyn
    if len(data)>10:
        ps = [[" HG","HG1"]]
        return proc_default(data,ps,"")
    else:
        ps = [["",""]]
        return proc_default(data,ps,"CYN")
    

def proc_asp(data): #13:aspp ,12:asp
    if len(data)>12:
        if args.r:
            t_data = []
            for i in data:
                if not('HD2' in i):t_data.append(i)
            return t_data
        else:
            ps = [["",""]]
            return proc_default(data,ps,"ASH")
    return data

def proc_asn(data): #14
    ps = [["1HD2","HD21"],["2HD2","HD22"]]
    return proc_default(data,ps,"")

def proc_arg(data): #24
    ps = [["1HH1","HH11"],["2HH1","HH12"],["1HH2","HH21"],["2HH2","HH22"]]
    return proc_default(data,ps,"")

aaproc = {'ARG':proc_arg,'ASN':proc_asn,'ASP':proc_asp,'CYS':proc_cys,
           'GLU':proc_glu,'GLN':proc_gln,'HIS':proc_his,'ILE':proc_ile,
           'LEU':proc_leu,'LYS':proc_lys,'SER':proc_ser, 'THR':proc_thr,'VAL':proc_val}


outfile = open(args.o,'w')

def processdata(arr):
    if len(arr)>0:
        resname = str(arr[0][17:20]).upper()
        arr = proc_NCterm(arr)
        data = aaproc.get(resname,defaultaa)(arr)
        for line in data:
            outfile.write(line)
    else:
        pass


res_data = []

prev_res_id = -1
with open(args.i,'r') as pdbfile:
    for line in pdbfile:
        if line.startswith("ATOM"):
            curr_res_id = int(line[22:26])
            if not(prev_res_id == curr_res_id):
                prev_res_id = curr_res_id 
                processdata(res_data)
                res_data = []
            res_data.append(line)
        else:
            processdata(res_data)
            outfile.write(line)
            res_data = []
    if len(res_data)>0:
        processdata(res_data)
        res_data = []

outfile.close()
