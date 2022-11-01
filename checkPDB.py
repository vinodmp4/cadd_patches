#!/usr/bin/python3

# Author:   Vinod M P
# Created:  June 5 2021
# Email:    mpvinod625@gmail.com
# License:  GPLv3

__lic__ = """
    CheckPDB - check PDB files for missing atoms other than Hydrogen.
    Copyright (C) 2021  Vinod M P

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__help__ = """

Linux Usage:   python3 checkpdb.py input.pdb
Windows Usage: python checkpdb.py input.pdb



RES|Total|protonation states  |  no Hydrogen
--------------------------------------------

ALA:10                              5
ARG:24                              11
ASN:14                              8
ASP:12  ASH:13                      8
CYS:11  CYN:10                      6
GLN:17                              9
GLU:15  GLH:16                      9
GLY:7                               4
HIS:17  HSE:17  HSD:17  HSP:18      10
ILE:19                              8
LEU:19                              8
LYS:22  LSN:21                      9
MET:17                              8
PHE:20                              11
PRO:14                              7
SER:11                              6
THR:14                              7
TRP:24                              14
TYR:21                              12
VAL:16                              7

hydrogen is responsible for protonation state difference
'no Hydrogen' is column having atom counts without hydrogen.
this program check whether the no Hydrogen atoms are there in positions.

"""

class pdb:
    def __init__(self):
        self.noHdata = {"ALA":5,"ARG":11,"ASN":8,"ASP":8,"CYS":6,"GLN":9,"GLU":9,"GLY":4,"HIS":10,"ILE":8,
                        "LEU":8,"LYS":9,"MET":8,"PHE":11,"PRO":7,"SER":6,"THR":7,"TRP":14,"TYR":12,"VAL":7}
        self.aminosequence = []
        self.aminoresids = []
        self.aminolength = []
        self.noHcounts = []
    
    def read(self,filename):
        prev_id,prev_alt,aacount,nohcount = -1,'*',0,0
        with open(filename,'r') as pdbfile:
            for record in pdbfile:
                if record[0:6].strip().upper() == 'ATOM':
                    if not(int(record[22:26])== prev_id):
                        if aacount>0:self.aminolength.append(aacount)
                        if nohcount>0:self.noHcounts.append(nohcount)
                        prev_id,prev_alt,aacount,nohcount = int(record[22:26]),record[26],1,1
                        self.aminosequence.append(record[17:20])
                        self.aminoresids.append(record[22:26])
                    else:
                        if not(record[26] == prev_alt):
                            if aacount>0:self.aminolength.append(aacount)
                            if nohcount>0:self.noHcounts.append(nohcount)
                            prev_alt,aacount,nohcount = record[26],1,1
                            self.aminosequence.append(record[17:20])
                        else:
                            if not(record[77].upper()=='H'):nohcount += 1
                            aacount += 1
            if aacount>0:self.aminolength.append(aacount)
            if nohcount>0:self.noHcounts.append(nohcount)

    def verifynoH(self):
        invalid_count = 0
        for i, x in enumerate(self.aminosequence):
            if not(self.noHcounts[i]==self.noHdata[x]):
                print(self.aminoresids[i], x, "required:", self.noHdata[x], "found:", self.noHcounts[i])
                invalid_count += 1
        if invalid_count>0:return False
        return True

import os,sys

arg = sys.argv
mypdb = pdb()
error = False
try:
    mypdb.read(arg[1])
except IndexError as ie:
    error = True
    print("Usage: python {0} input.pdb".format(os.path.basename(sys.argv[0])))
except:
    error = True
    print("Unknown error contact Vinod")
if not(error):
    print(__lic__)
    print('-'*25+'\n'+"Checking atoms other than hydrogen\n"+'-'*25)
    if not(mypdb.verifynoH()):print("-"*25,'\nError in pdb file.')
    else:print("-"*25,'\nPdb file is successfully verified.')
