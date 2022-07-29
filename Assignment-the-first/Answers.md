# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | Read1 | 101 | 33 |
| 1294_S1_L008_R2_001.fastq.gz | Index1 | 8 | 33 |
| 1294_S1_L008_R3_001.fastq.gz | Index2 | 8 | 33 |
| 1294_S1_L008_R4_001.fastq.gz | Read2 | 101 | 33 |

2. Per-base NT distribution
  i. Turn in the 4 histograms.  
    
    1. Read1
    
    ![Distribution_R1](https://user-images.githubusercontent.com/89626045/181821802-a2c3e5ed-31b2-4848-a1e5-7638f15bc338.jpeg)

    2. Index1
    
    ![Distribution_R2](https://user-images.githubusercontent.com/89626045/181821901-284278a8-f624-41eb-9d0a-30c8c14f0a62.jpeg)

    3. Index2
    
    ![Distribution_R3](https://user-images.githubusercontent.com/89626045/181822003-37c95768-a453-43ca-92e1-69f8f0a4ae22.jpeg)

    4. Read2 
    
    ![Distribution_R4](https://user-images.githubusercontent.com/89626045/181822092-b560a0f2-5124-4db6-9288-550a7ef1b712.jpeg)

   ii. What is a good quality score cutoff for index reads and biological read pairs to utilize for sample identification and downstream analysis, respectively?
   For biological reads I would asign a quality score cutoff of 20 since it's not that important for us since during alignment if a read doesn't match the base sequence it will be discarded.
   For Index reads I'm proposing using the quality score cutoff of 20, this is because the sequences for indexes are short (8) and after doing some revising of indexes sequences they differ by at least 3 nucleotides so the possibility of incorrectly asigning a barcode would be *very low*
   
   iii.How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. 
   ```
   zcat 1294_S1_L008_R2_001.fastq.gz 1294_S1_L008_R3_001.fastq.gz | sed -n "2~4p" | grep "N" | wc -l
   
   Result.- 7304664
   ```
    
    
## Part 2
1. Define the problem
    We have four files that each have a record corresponding to a cluster; R1 corresponds to the biological read (sense); I1 corresponds to the index for biological read 1(sense); R2 corresponds to the biological read (anti-sense); I2 corresponds to the index for biological read 2 (anti-sense). We need to clasify the biological reads (R1 & R2) by matching indexes; hopped indexes and unknown or low quality indexes. Since if we want to sequence only the data with matching barcodes which would correspond to only one cluster and that can be aligned to our corresponding genome sequence.
    

2. Describe output
  We will obtain two files per matched index (one per each read file), since we have 24 known indexes we would obtain 48 files (24 R1 & 24 R2). Two files for hopped indexes (1 R1 & 1 R2) and two files for unknown (1 R1 & 1 R2). 
  In our test data we will have 6 output files since we will only test 1 matched index (1 R1; 1 R2), one test for hopped index (1 R1; 1 R2), and finally one test for unkown (1 R1; 1 R2)
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
  Inputed on folder "Test_Files"

4. Pseudocode
  Was uploaded as a separate file in the repository (higher level)
  
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
