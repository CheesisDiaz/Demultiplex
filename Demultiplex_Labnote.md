# Lab Notebook for Bi621
### Isis Diaz

## Demultiplex The First
### | July 26 of 2022 |
#### Develop a strategy to de-multiplex samples to create 48 FASTQ files that contain acceptable index pairs (read1 and read2 for 24 different index pairs), two FASTQ files with index-hopped reads-pairs, and two FASTQ files undetermined (non-matching or low quality) index-pairs.
#### Part1 Distribution per position Graph
Collaborators:
Leslie Coonrod <coonrod@uoregon.edu>
Programs Used:
Python 3.10.4
Modules Used:
gzip
bioinfo

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

After performing the first data exploration next we need to determine which are biological reads and which are indexes and they are as follows:
```
1294_S1_L008_R1_001.fastq.gz - Biological Read1 
1294_S1_L008_R2_001.fastq.gz - Index Read1
1294_S1_L008_R3_001.fastq.gz - Index Read2 (antisense)
1294_S1_L008_R4_001.fastq.gz - Biological Read2
```
Now to start with Part1 we need to generate a per base distribution of quality scores for read1, read2, index1, and index2, this means that we need to obtain the sequence of each record. Since the file we are reading we need to gzip open the file knowning that a fastq file has four lines per record we can use the method for reading files readfile() and assign a name to each line like so:
```
Head = fi.readline().strip()
        if Head == "":
            break
        Seq = fi.readline().strip()
        Sep = fi.readline().strip()
        Qsc = fi.readline().strip()
```
I'm using a while True: Loop so this needs to stop once we finish the file, I accomplish this by breaking when we see an empty line (""), this is done in Head since that would be the value where we would see the empty space.

Now that we have identified the sequence we can work on obtaining the quality score of each position. for this we will need to import the bioinfo.py module to use the convert phred function.
I first wanted to work with a 2D numpy array and it worked on my small file but for the big one it was too much information and the program exit, so i change the approach to do a sumation per position in a 1D numpy array.
```
for indx,letter in enumerate(Seq):
            p_score = bioinfo.convert_phred(letter) #For letter in each line a p_score will be calculated
            pos_array[indx] += p_score #pscore per position will be summed in the array
```
Then to obtain the mean we would have to loop over our array and for each value divide by the total ammount of records 
```
means = []
for score in pos_array:
    means.append(score/l)
```
The only thing that we need to create the graphs is obtaining all of the positions which is easy to do, by using numpy.arange to how many positions we need

Having our distribution and positions we can create a graph using matplotlib for bars 
```
plt.bar(pos, means, color = 'slategrey') #To change the color of the plot
plt.title('Distribution Quality Scores') #Main title
plt.xlabel('Position of Read') #Title of x Axis
plt.ylabel('Mean Quality Score') #Title of the y Axis
plt.savefig(o) #The file will be saved to the name that we put here, I decided to do it through argparse.
```

After the code was complete i perform tests in one of the files to see if any error appeared. I ran the program and i had an error over matplotlib
```
Traceback (most recent call last):
  File "/gpfs/projects/bgmp/isisd/bioinfo/Bi622/Demultiplex/Assignment-the-first/./Distribution_hist.py", line 2, in <module>
    import matplotlib.pyplot as plt
ModuleNotFoundError: No module named 'matplotlib'
```
I realized that my bgmp_py310 environment didn't have matplotlib installed so I did the following way
```
conda activate bgmp_py310

conda install matplotlib
```

I ran the the code again and i had a positive result, so the next thing was include argparse to be able to use the program for several files
```
    "--length", help="How many reads are in this file?"
    "--file", help="Specify the filename to analyze (FASTQ format)"
    "--output", help="Specify the output filename for the graph"
```
Next step was to create a batch program to run the code on Talapas, I added the shebang and all of the required codes to run in a working node. I activated the python3 environment
```
conda activate bgmp_py310
```
and I ran the four files in the same batch script by doing the four argparse

Example:
```
#Read1
/usr/bin/time -v ./Distribution_hist.py \
    -p 101 \
    -l 363246735 \
    -f "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz" \
    -o "Distribution_R1(2).jpg"
echo "Finsh on Read1" #This is to keep control of how the program is advancing through the files
#Index1
/usr/bin/time -v ./Distribution_hist.py \
    -p 8 \
    -l 363246735 \
    -f "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz" \
    -o "Distribution_R2(2).jpg"
echo "Finish on Index1"
```

The resulting run was:
```
Command being timed: "./Distribution_hist.py -p 101 -l 363246735 -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -o Distribution_R1(2).jpg"
	User time (seconds): 12752.75
	System time (seconds): 1.51
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 3:32:41
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 62768
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 78474
	Voluntary context switches: 2089
	Involuntary context switches: 3215
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
Finsh on Read1
	Command being timed: "./Distribution_hist.py -p 8 -l 363246735 -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -o Distribution_R2(2).jpg"
	User time (seconds): 1386.49
	System time (seconds): 0.31
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 23:11.18
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 59300
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 37411
	Voluntary context switches: 2112
	Involuntary context switches: 409
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
Finish on Index1
	Command being timed: "./Distribution_hist.py -p 8 -l 363246735 -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -o Distribution_R3(2).jpg"
	User time (seconds): 1367.45
	System time (seconds): 0.33
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 22:53.87
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 59320
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 36581
	Voluntary context switches: 2569
	Involuntary context switches: 631
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
Finish on Index2
	Command being timed: "./Distribution_hist.py -p 101 -l 363246735 -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -o Distribution_R4(2).jpg"
	User time (seconds): 12787.82
	System time (seconds): 1.71
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 3:33:13
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 59624
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 62127
	Voluntary context switches: 2088
	Involuntary context switches: 3208
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
Complete
```
For the final part of Part1 it was necessary to obtain how many indexes have undetermined (N) base calls. I determined this by doing the following command in the CL. 
```
zcat 1294_S1_L008_R2_001.fastq.gz 1294_S1_L008_R3_001.fastq.gz | sed -n "2~4p" | grep "N" | wc -l
   
Result.- 7304664
```

### | July 27 of 2022 |
#### Part 2. Develop an algorithm to de-multiplex the samples

When i was task to start the pseudocode for the algorithm i realized that I didn't understand how to obtain the index for revising if they were matched. After revising it with Leslie Coonrod I understood what i needed to do. So i started to write all the checks i would do to the data. The first draft was really short only checking in a very general way.

```
Is there an N in any index; Redirect to Unknown file (Change header)


If index 1 or 2 not in the know index; Redirect to Unknown file (Change header)

Quality score is bellow the cutoff; Redirect to Unknown file (Change header)

Is Index 1 equal to rev.complement of index2; Redirect to file with name of index 1 (Change header)

Indez 1 is diff to rev.complement of index 2; Redirect to hopped (Change header)

```
### | July 29 of 2022 |
Once i had the basic structure of the flow of the pseudocode I worked on building a more comprehensible step by step to better help me when I'm actually running the program. And writing the pseudocode help me think of which functions i could construct to better help me organize my program. From which I constructed the following functions
```
PHRED SCORING - For obtaining the phred score with the intention to use this for the Quality Score Cutoff

REVERSE COMPLEMENT - Obtain the reverse complement for Index2; To evaluate for Dual Match Index or Index Hopping

RENAMING HEADERS - This will create the new headers including both indexes

READFILE - This will read through the file and obtain a record to review

UNKNOWN INDEX - This will determine if there is an N in the index
```

Its important to mention that the only function that i didn't use was the Unknown Index, even though i did created it wasn't necessary.

The last thing i performed for Demultiplex the first was the test files and expected outcomes to test my code with.

## Demultiplex The Second
### | August 1st of 2022 |

In this part of the assignment we were required to read our colleagues pseoudocode and give notations. ALl my colleagues had great pseudocode that gave me ideas for when I continue to write pseudocode and also made me realize i didn't consider some steps as :
- Counting records per file type (Matched, Hopped, Unknown)

- Open all the files where records will be redirect it

## Demultiplex The Third
### | August 3rd of 2022 |

The first thing I started developing was the functions that i wrote for Demultiplex the First and tested each of them to determine if they were working correctly individually.
When working on the function of readfiles i was trying to determine how to have all records to be able to compare each file, but i was creating a list with all the records. This would end up taking too much memory and with the help of Jason Sydes i worked on the function that would return a list of the four lines of the record. To make sure that it would look a record at a time the function was inputed on a loop, so every loop a complete record per file would be revised.

During the Demultiplex open lab I also worked on a method of how to open all the files, my first approach was the use of a tuple, but I only did the tuple of all the file names. The problem of this approach is that when performing the looping I didn't know how to actually open the file, it was suggested to me by some colleagues to use a directory. So I created a directory where the key is the name of the file (one for R1 and for R2) and the value was open(filename,"r") and thats how i fixed the opening of the files.

## Demultiplex The Third
### | August 5th of 2022 |

Once my functions worked correctly, i could open the files the following step was to actually write the conditions for my code. 

The first thing was to have both indexes so I can do the neccesary comparisons. I wrote a function to obtain the reverse complement so i gave a new variable for the reverse complement of the read2 since thats antisense <-. And with that i created a function for new header. both will be applied to all of the files.

The first comparison i performed is to revise if any of the indexes contain an N. I wrote a function that would return boolean True if it contain any Ns, it took me a little bit to implement as i was having issues with the OR argument. I was doing the following
```
If N in index1 or index2:
do
```
But this wasn't doing the comparison i need it, After researching online I found that the correct comparison is the following
```
If N in index1 or N in index2:
do
```

I incorporated this function to the code and the next comparison is if any index is not in my known indexes it should be printed to the unknown files. This is where i realized my function N wasn't necessary as if there is an N in any index it won't be in the known indexes. I deleted that part of my code and change to only revise if they are in my set of known indexes:
```
If index1 not in known_indx or index2 not in known_indx
do
```
* Note: Every part i wrote i ran with my test files to see their basic performance.*

The next comparison was to look at the quality cutoff, for which i created a function that would return a True boolean if any average phred score of index1 or index2 was below of the cutoff
```
if i1_score < qscr_cutoff or i2_score < qscr_cutoff:
        return True
```

### | August 6th of 2022 |

And in my code when True the file would be written to unknown. In this point i realized that maybe i should have a count of this cutoff aside from unknown. I created a directory for Unknown, Matched, Hopped and Cutoff to have a count of each type of record like so
```
counts["Cutoff"] +=1 #This when the file is redirected to Unknown by cutoff
```
Finally the last comparison once all of the index are known and pass the quality score cutoff we can see if the files are Matched or Hopped 
```
if index1 == rev(index2)
counts ["Matched"] += 1
```

Once i believed my code was correct i worked on the argparse for all my required arguments
- read1
- index1
- read2
- index2
- outputfolder
- qcutoff
- known indexes
- records

The last thing was worked on the stats file which i decided to include in this code. I planned to report the following:

- Total Count of Records
- Total Count of Dual Matched Indexes
- Total Count of Hopped Indexes
- Total Count of Bad Quality Reads
- Total Count of Unknown Indexes
- All of the Dual Matched Count and percentage
- All of the Index Hopped Count and percentage

### | August 8th of 2022 |

I thought my code was ready but I was scared of running in the actual files since i hadn't done a trial with a bigger set than my test files. Here are all of the errors i corrected with the help of Leslie Coonrod for my file to run correctly

- My shebang for the python file wasn't correct and while running the program the language wasn't identified correctly
- Parser arguments where incorrect; Missing def get_args(): and return parser.parse_args(); had argument description instead of help.
- gzip open was reading in binary and showing errors for my functions, should have been
```
gzip open(file.gz, "rt")
```
```
Traceback (most recent call last):
  File "/gpfs/projects/bgmp/isisd/bioinfo/Bi622/Demultiplex/Assignment-the-third/./Demultiplex.py", line 163, in <module>
    new_i2 = rev_complement(i2[1]) #index 2 sequence reverse complement
  File "/gpfs/projects/bgmp/isisd/bioinfo/Bi622/Demultiplex/Assignment-the-third/./Demultiplex.py", line 59, in rev_complement
    rev_com += rev[letter]
KeyError: 78
Command exited with non-zero status 1
	Command being timed: "./Demultiplex.py -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -i1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -i2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -i /projects/bgmp/shared/2017_sequencing/indexes.txt -q 30 -rec 363246735 -o /projects/bgmp/isisd/bioinfo/Bi622/Demultiplex/Assignment-the-third/output_test"
	User time (seconds): 0.01
	System time (seconds): 0.02
	Percent of CPU this job got: 70%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.06
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 26588
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 4403
	Voluntary context switches: 237
	Involuntary context switches: 2
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 1

```

For stats file
- The parenthesis for rounding the percentages were incorrectly plased and that was causing an error on the string i wanted to print; Example
```
fs.write("Total Count of Dual Matched Indexes: "+ str(c_mat) + " - " + str(round(c_mat/lines * 100, 2)) + "%\n")
```
```
Traceback (most recent call last):
  File "/gpfs/projects/bgmp/isisd/bioinfo/Bi622/Demultiplex/Assignment-the-third/./Demultiplex.py", line 201, in <module>
    fs.write("Total Count of Dual Matched Indexes: "+ str(counts["Match"]) + "\t" + str(round((counts["Match"]/ lines) *100), 2) + "%\n")
TypeError: str() argument 'encoding' must be str, not int
Command exited with non-zero status 1
	Command being timed: "./Demultiplex.py -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -i1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -i2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -i /projects/bgmp/shared/2017_sequencing/indexes.txt -q 30 -rec 363246735 -o /projects/bgmp/isisd/bioinfo/Bi622/Demultiplex/Assignment-the-third/output_test"
	User time (seconds): 3684.78
	System time (seconds): 44.16
	Percent of CPU this job got: 93%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:06:16
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 245524
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 601231
	Voluntary context switches: 48131
	Involuntary context switches: 2212
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 1
```
- For what i wanted to print individually each index for dual and hopped i needed to create another dictionary

After correcting all of those errors I was ran my program succesfully, here the results of timing for the program:
```
	Command being timed: "./Demultiplex.py -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -i1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -i2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -i /projects/bgmp/shared/2017_sequencing/indexes.txt -q 30 -rec 363246735 -o /projects/bgmp/isisd/bioinfo/Bi622/Demultiplex/Assignment-the-third/output_test"
	User time (seconds): 3742.31
	System time (seconds): 94.51
	Percent of CPU this job got: 86%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:13:54
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 245512
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 296336
	Voluntary context switches: 49082
	Involuntary context switches: 5378
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
```

Last thing to finish the Demultiplex assignment is to zip all the files, for this I used pigz
```
/usr/bin/time -v for file in output_test/* ; \
    do pigz $file ; \
    done
```