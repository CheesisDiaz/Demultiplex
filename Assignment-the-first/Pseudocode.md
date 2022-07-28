#PSEUDOCODE FOR DEMULTIPLEX ASSIGNMENT THE FIRST

Perform a for loop to read the 4 files at a time
Create an empty dictionary
while reading Index1 the Sequence line should be input as a key in the dictionary
For Index2 also take the Sequence line and obtain the reverse complement (now mentioned as Index2*) #(check passed lectures on jupyter notebook probably day 2) Input that on the dictionary as a value for its corresponding Index1 

If Index1 or Index2 contain any "N" move the Read1 (record) to "Unknown_R1.fq" and move Read2 (record) to "Unknown_R2.fq".while while redirecting change the header of Read1 and Read2 record to include Index1:Index2*

If Index1 and Index2* is in known indexes:
    Revise if Index1 and Index2* are equal if they are:
        Redirect the Read1 record to "Index1_R1.fq" and Read2 record to "Index1_R2.fq". while redirecting change the header of Read1 and Read2 record to include Index1:Index2*
    If Index1 and Index2* are not equal:
        Redirect the Read1 record to "hopped_R1.fq" and Read2 record to "hopped_R2.fq". while while redirecting change the header of Read1 and Read2 record to include Index1:Index2*
ELSE if the Index1 and Index2* is not in known indexes:
    Redirect the Read1 record to "Unknown_R1.fq" and Read2 record to "Unknown_R2.fq". while while redirecting change the header of Read1 and Read2 record to include Index1:Index2*