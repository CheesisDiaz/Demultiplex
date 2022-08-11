#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --time=0-10:00:00
#SBATCH --job-name=demux3

conda activate bgmp_py310


/usr/bin/time -v ./Demultiplex.py \
    -r1 "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz" \
    -r2 "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz" \
    -i1 "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz" \
    -i2 "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz" \
    -i "/projects/bgmp/shared/2017_sequencing/indexes.txt" \
    -q 30 \
    -rec 363246735 \
    -o "/projects/bgmp/isisd/bioinfo/Bi622/Demultiplex/Assignment-the-third/output_test"
