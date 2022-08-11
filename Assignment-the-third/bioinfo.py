#!/usr/bin/env bash
# Author: <Isis_Diaz> <isisd@uoregon.edu>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.3"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNAbases = set('ATGCNatcgn')
RNAbases = set('AUGCNaucgn')

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    phred = (ord(letter)) - 33
    return(phred)

#autograder tests, do not change
if "__name__" == "__main__":
    """Check that convert_phred returns the correct value for several different inputs"""
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

def qual_score(phred_score: str):
    """for every letter the function convert_phred obtains the score and for every 
    itteration it adds the value to tot_scr to calculate the average against the length of the phred_score string"""
    tot_scr=0 #Sum of all scores
    for letter in phred_score:
        ind_scr = convert_phred(letter)#this will give the value of each individual phred score
        tot_scr += ind_scr #this will add the value of each individual phred score to the total score
        avr_scr = tot_scr/len(phred_score) #to obtain the average we divide the sum of scores with the length of the string
    return(avr_scr)

if "__name__" == "__main__":
    assert qual_score("phred_score") == 37.62105263157895, "correct average phred score"

def validate_base_seq(seq,RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    return set(seq)<=(RNAbases if RNAflag else DNAbases)

if "__name__" == "__main__":
    assert validate_base_seq("AATAGAT") == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("Hi there!") == False, "Validate base seq fails to recognize nonDNA"
    assert validate_base_seq("Hi there!", True) == False, "Validate base seq fails to recognize nonDNA"
    print("Passed DNA and RNA tests")

def gc_content():
    '''Returns GC content of a DNA sequence as a decimal between 0 and 1.'''
    DNA = DNA.upper()         #Make sure sequence is all uppercase
    Gs = DNA.count("G")       #count the number of Gs
    Cs = DNA.count("C")       #count the number of Cs
    return (Gs+Cs)/len(DNA)

if "__name__" == "__main__":
    assert gc_content("GCGCGC") == 1
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATGCAT") == 0.5
    print("You have the correct percentage of CGs!")

def oneline_fasta(input_file: str, out_file: str):
    '''This function takes two file names (input and output) which converts an unwrapped fasta file
    to a two line convention'''
    data = []
    header = ""
    count = 0
    with open(input_file,"r") as fp:
        for line in fp:
            line  = line.strip()
            if ">" in line: #To identify the header
                if header == "": #For the first line prot_id wont have a value
                    header = line
                else:    #For the rest of the lines
                    seq = "".join(data)
                    data.clear()
                    count += 1
                    print(f"{header}\n{seq}", file=out_file)
                    header = line
            else:
                data.append(line)
        seq = "".join(data)
        data.clear()
        count += 1
        print(f"{header}\n{seq}", file=out_file)
    return (count)

if "__name__" == "__main__":
    assert qual_score("test_file.fa") == 4, "correct ammount of lines"
    print("Unwrapped the Fasta File correctly!")
