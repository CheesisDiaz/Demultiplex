#!/usr/bin/env python
#MODULES USED
import bioinfo
import gzip
import argparse

#ARGPARSE

def get_args():
    parser = argparse.ArgumentParser(description="This program will take in four fastq files with 2 biological reads and 2 index reads and will create a filen per matched index files for unknown and index hopped")
    parser.add_argument("-r1", "--read1", help="Input the filename for Read 1 (fastq)", type=str, required=True)
    parser.add_argument("-i1", "--index1", help="Input the filename for Index 1 (fastq)", type=str, required=True)
    parser.add_argument("-r2", "--read2", help="Input the filename for Read 2 (fastq)", type=str, required=True)
    parser.add_argument("-i2", "--index2", help="Input the filename for Index 2 (fastq)", type=str, required=True)
    parser.add_argument("-o", "--outputfolder", help="Input the output folder directory for results (must already exist)", type=str, required=True)
    parser.add_argument("-q", "--qcutoff", help="Input the Quality Score Cutoff for Index", type=int, required=True)
    parser.add_argument("-i", "--indexes", help="Input the filename for all known indexes", type=str, required=True)
    parser.add_argument("-rec", "--records", help="Input how many records are being revised (one file)", type=int, required=True)
    return parser.parse_args()

args = get_args()
R1 = args.read1
I1 = args.index1
R2 = args.read2
I2 = args.index2
outfolder = args.outputfolder
qscr_cutoff = args.qcutoff
KIndx = args.indexes
lines = args.records



#VARIABLES
counts ={"Match":0, "Hopped":0, "Unknown":0, "Cutoff":0}


#FUNCTIONS UTILIZED

def readfiles(f: str) -> list:
    """This function will read through a file and will create a list per record 
    [Head, Seq, Sep, Qsc]"""
    head = f.readline().strip()
    seq = f.readline().strip()
    sep = f.readline().strip()
    qsc = f.readline().strip()
    return [head, seq, sep, qsc]

rev = {"A": "T", "C": "G", "T": "A", "G":"C", "N" : "N"}
def rev_complement(seq: str) -> str:
    """This function will read a sequence and return it's reverse complement"""
    rev_com = ""
    for letter in seq:
        rev_com += rev[letter]
    return(rev_com[::-1])

def new_header(r1:list, r2:list, i1:list, i2:list) -> list:
    """This function will take 4 records and update the header with the indx and
    its reverse complement for the biological reads"""
    index1 = i1[1]
    index2 = rev_complement(i2[1])
    r1[0] = r1[0] + ":" + index1 + "-" + index2
    r2[0] = r2[0] + ":" + index1 + "-" + index2
    return(r1,r2)

def n_indx(indx1:str, indx2:str) -> bool:
    """This function will take two index and determine if the index contains an N"""
    if "N" in indx1 or "N" in indx2:
        return True
    else:
        return False

def avr_scr(seq:str) -> float:
    """This function will take a sequence record and will obtain the average score 
    for that record"""
    sum = 0
    for letter in seq:
        sum += bioinfo.convert_phred(letter)
        length = len(seq)
    average = sum/length
    return average

def cutoff(seqi1:str, seqi2:str) -> bool:
    """This function will take in the index reads 1 and 2, and base on its average score
    will return a True statment if its below the Quality score cutoff"""
    i1_score = avr_scr(seqi1)
    i2_score = avr_scr(seqi2)
    if i1_score < qscr_cutoff or i2_score < qscr_cutoff:
        return True
    else:
        return False

# a="EEEEE"
# b="#####"
# c="###EE"
# d="BBBBB"
# if cutoff(a,d):
#     print("nothing")
# else:
#     print("something")

#Creating a set for the known indexes sense
dual_mat = {}
ind_hop = {}
know_indx = set()
with open(KIndx,"r") as fk:
    for line in fk:
        line = line.strip().split()
        if "sample" not in line:
            indx = line[4] #For actual file
            know_indx.add(indx)
            


#Opening All files
all_files = []
ext1 = "_R1.fq"
ext2 = "_R2.fq"
#List of all output files with index names
files_to_create = {}
for indx in know_indx:
    fn1 = outfolder + "/" + indx + ext1
    fn2 = outfolder + "/" + indx + ext2
    fr1 = indx + "_R1"
    fr2 = indx + "_R2"
    files_to_create[fr1] = open(fn1,"w")
    files_to_create[fr2] = open(fn2,"w")


#Adding unknown and hopped to list
unk1 = outfolder + "/unknown" + ext1
unk2 = outfolder + "/unknown" + ext2
hop1 = outfolder + "/hopped" + ext1
hop2 = outfolder + "/hopped" + ext2
files_to_create["unknown_R1"] = open(unk1,"w")
files_to_create["unknown_R2"] = open(unk2,"w")
files_to_create["hopped_R1"] = open(hop1,"w")
files_to_create["hopped_R2"] = open(hop2,"w")

fr1 = gzip.open(R1,"rt")
fi1 = gzip.open(I1,"rt")
fi2 = gzip.open(I2,"rt")
fr2 = gzip.open(R2,"rt")

#append to all files
all_files.append(fr1)
all_files.append(fi1)
all_files.append(fi2)
all_files.append(fr2)
 

i = 0
while i < lines:
    r1 = readfiles(fr1)
    i1 = readfiles(fi1)
    i2 = readfiles(fi2)
    r2 = readfiles(fr2)
    #reverse complement of i2
    new_i2 = rev_complement(i2[1]) #index 2 sequence reverse complement
    new_i1 = i1[1] #To facilitate the identification of index1 sequence
    if new_i1 not in know_indx or new_i2 not in know_indx:
        a,b = new_header(r1,r2,i1,i2)
        files_to_create["unknown_R1"].write("\n".join(a)+"\n")
        files_to_create["unknown_R2"].write("\n".join(b)+"\n")
        counts['Unknown'] += 1
    elif cutoff(i1[3], i2[3]): #Should it be if or elif?
        a,b = new_header(r1,r2,i1,i2)
        files_to_create["unknown_R1"].write("\n".join(a)+"\n")
        files_to_create["unknown_R2"].write("\n".join(b)+"\n")
        counts["Cutoff"] += 1
    elif new_i1 == new_i2:
            a,b = new_header(r1,r2,i1,i2)
            key1 = new_i1+"_R1"
            key2 = new_i1+"_R2"
            files_to_create[key1].write("\n".join(a)+"\n")
            files_to_create[key2].write("\n".join(b)+"\n")
            counts['Match'] += 1
            ind = new_i1 + "-" + new_i2
            if ind not in dual_mat.keys():
                dual_mat[ind] = 1
            else:
                dual_mat[ind] += 1
    else:
        a,b = new_header(r1,r2,i1,i2)
        files_to_create["hopped_R1"].write("\n".join(a)+"\n")
        files_to_create["hopped_R2"].write("\n".join(b)+"\n")
        counts['Hopped'] += 1
        ind = new_i1 + "-" + new_i2
        if ind not in ind_hop.keys():
                ind_hop[ind] = 1
        else:
            ind_hop[ind] += 1
    i+=1

#Loop for closing all the files
for f in files_to_create.values():
    f.close()

for f in all_files:
    f.close

stat = outfolder + "/stats.md"
c_mat = counts["Match"]
c_hop = counts["Hopped"]
c_unk = counts["Unknown"]
c_cut = counts["Cutoff"]

with open(stat, "w") as fs:
    fs.write("Stats from Demultiplexing\n\n")
    fs.write("Total Count of Records: " + str(lines) + "\n")
    fs.write("Total Count of Dual Matched Indexes: "+ str(c_mat) + " - " + str(round(c_mat/lines * 100, 2)) + "%\n")
    fs.write("Total Count of Hopped Indexes: " + str(c_hop) + " - " + str(round(c_hop/lines *100, 2)) + "%\n")
    fs.write("Total Count of Bad Quality Reads: " + str(c_cut) + " - " + str(round(c_cut/lines *100, 2)) + "%\n")
    fs.write("Total Count of Unknown Indexes: " + str(c_unk) + " - " + str(round(c_unk/lines *100, 2)) + "%\n\n")
    fs.write("Dual Matched Indx \n Counts \n Percentage \n")
    for key in dual_mat:
        fs.write(str(key) + "\t" + str(round(dual_mat[key]/lines * 100, 2)) + "%\n")
    fs.write("Hopped Index \n Counts \n Percentage \n")
    for key in ind_hop:
        fs.write(str(key) + "\t" + str(round(ind_hop[key]/lines * 100, 2)) + "%\n")



