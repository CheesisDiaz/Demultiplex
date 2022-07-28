#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import bioinfo
import gzip
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="A program to obtain a graph of the Quality Mean Score by position of sequence of fastq file")
    parser.add_argument("-p", "--position", help="How many bps are per sequence?", required=True, type=int)
    parser.add_argument("-l", "--length", help="How many reads are in this file?", required=True, type=int)
    parser.add_argument("-f", "--file", help="Specify the filename to analyze (FASTQ format)", required=True, type=str)
    parser.add_argument("-o", "--output", help="Specify the output filename for the graph", required=True, type=str)
    return parser.parse_args()

args = get_args()
bp=args.position
l=args.length
f=args.file
o=args.output

#For biology reads files
pos_array = np.zeros(bp, dtype=float)
with gzip.open(f, "rt") as fi:
    count = 0
    while True:
        Head = fi.readline().strip()
        if Head == "":
            break
        Seq = fi.readline().strip()
        Sep = fi.readline().strip()
        Qsc = fi.readline().strip()
        for indx,letter in enumerate(Seq):
            p_score = bioinfo.convert_phred(letter) #For letter in each line a p_score will be calculated
            pos_array[indx] += p_score
        count += 1

means = []
for score in pos_array:
    means.append(score/l)

pos = np.arange(bp)


plt.bar(pos, means, color = 'slategrey')
plt.title('Distribution Quality Scores')
plt.xlabel('Position of Read')
plt.ylabel('Mean Quality Score')
plt.savefig(o)

