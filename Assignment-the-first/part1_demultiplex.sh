#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=1
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --time=0-10:00:00
#SBATCH --job-name=mean_qualityscr2

conda activate bgmp_py310
#Read1
/usr/bin/time -v ./Distribution_hist.py \
    -p 101 \
    -l 363246735 \
    -f "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz" \
    -o "Distribution_R1(2).jpg"
echo "Finsh on Read1"
#Index1
/usr/bin/time -v ./Distribution_hist.py \
    -p 8 \
    -l 363246735 \
    -f "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz" \
    -o "Distribution_R2(2).jpg"
echo "Finish on Index1"
#Index2
/usr/bin/time -v ./Distribution_hist.py \
    -p 8 \
    -l 363246735 \
    -f "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz" \
    -o "Distribution_R3(2).jpg"
echo "Finish on Index2"
#Read2
/usr/bin/time -v ./Distribution_hist.py \
    -p 101 \
    -l 363246735 \
    -f "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz" \
    -o "Distribution_R4(2).jpg"
echo "Complete"