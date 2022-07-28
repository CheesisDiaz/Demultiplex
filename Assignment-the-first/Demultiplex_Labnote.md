#Lab Notebook for Bi621
###Isis Diaz

##Demultiplex The First
###| July 26 of 2022 |
####develop a strategy to de-multiplex samples to create 48 FASTQ files that contain acceptable index pairs (read1 and read2 for 24 different index pairs), two FASTQ files with index-hopped reads-pairs, and two FASTQ files undetermined (non-matching or low quality) index-pairs.
Collaborators:
Kaetlyn Gibson <helioskaet@gmail.com>
Leslie Coonrod <coonrod@uoregon.edu>
Anh Vo <athuyvo@gmail.com>
Programs Used:
Python 3.10.4
Modules Used:

The first thing that was performed was the data exploration where i performed the following commands to understand the database I'm gonna parse through and to start thinking of an strategie before starting to work on any code:
Read the README file
```
cat README.txt
```
See the format of the indexes file
```
cat indexes.txt
```
See the format of the reads files (Example on Read1)
```
zcat 1294_S1_L008_R1_001.fastq.gz | less -S
```
Obtain the sequence lines that are on the files to determine strategie:
```
zcat 1294_S1_L008_R1_001.fastq.gz | wc -l
1452986940

363246735 sequences (divided by 4 the result of that command)
```
To obtain the length of the sequence read (example for Read1)
```
zcat 1294_S1_L008_R1_001.fastq.gz | head -2 | tail -1 | wc
102
<consider the /n character, 101 nucleotides>
```