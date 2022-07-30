# PSEUDOCODE FOR DEMULTIPLEX ASSIGNMENT THE FIRST

- Perform a for loop to read the 4 files at a time
- Create an empty dictionary
- Read the file of known indexes and each index should be inputed as a key, for the value we should obtain the reverse complement

- For Index2 also take the Sequence line and obtain the reverse complement (now refered to as Index2*)

- If Index1 or Index2 contain any "N" 
    
    Move the Read1 (record) to "Unknown_R1.fq" and move Read2 (record) to "Unknown_R2.fq".while while redirecting change the header of Read1 and Read2         record to include Index1:Index2*

- If the Index1 and Index2* is not in the dictionary (*known indexes*):
        
    Redirect the Read1 record to "Unknown_R1.fq" and Read2 record to "Unknown_R2.fq". 
     while while redirecting change the header of Read1 and Read2 record to include Index1:Index2*
        
- If Index1 and Index2* is in the dictionary (*known indexes*):
    Iterate over each letter of the Index records and obtain Average Quality Score per record
   - If Quality Score is less than Quality Score Cutoff
   
     Redirect the Read1 record to "Unknown_R1.fq" and Read2 record to "Unknown_R2.fq". 
     while while redirecting change the header of Read1 and Read2 record to include Index1:Index2*
     
   - If Quality Score is more than the Quality Score Cutoff

        - Revise if Index1 and Index2* are equal if they are:
            
            Redirect the Read1 record to "Index1_R1.fq" and Read2 record to "Index1_R2.fq". 
            while redirecting change the header of Read1 and Read2 record to include Index1:Index2*
            
        - If Index1 and Index2* are not equal:
            
            Redirect the Read1 record to "hopped_R1.fq" and Read2 record to "hopped_R2.fq". 
            while while redirecting change the header of Read1 and Read2 record to include Index1:Index2*
            
