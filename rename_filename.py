#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse
# Pythono3 code to rename multiple  
# files in a directory or folder
  
import os 
    
def rename_files(directory, filename_prefix, filename_ext, dry_run = False, counter = 0):
    """
    Loop throught files and rename them keeping a trace of the old names
    """
    i = counter
    new_filenames = {}
    for src_filename in os.listdir(directory): 
        # from filename to prefix_0.txt
        number_prefix = "{:02d}".format(i)
        dst_filename =  filename_prefix + number_prefix + "." + filename_ext
        
        src = os.path.join(directory, src_filename)
        dst = os.path.join(directory, dst_filename)

        if (dry_run == False): os.rename(src, dst)
        new_filenames[src_filename] = dst_filename
        i += 1

    return new_filenames

def save_new_names_as_csv(new_filenames, csv_filename):

    with open(csv_filename, 'w', newline='') as file:
        # iterate over new_filenames (A DICTIONARY)
        for old_filename in new_filenames.keys():
            # write old name;new name
            file.write(old_filename +";" + new_filenames[old_filename]+"\n")

    # print(new_filenames)

def main(): 
    """
    Function to rename multiple files 
    """

    directory = "C:\\Users\\kogkitse\\Documents\\Post-doc\\corpus_sans_etiquetes\\visiautrices\\"
    filename_prefix = "visiautrices_"
    filename_ext =  "xml"
    new_names = rename_files(directory, filename_prefix, filename_ext, False)

    csv_filename = "visiautrices_filenames.csv"
    save_new_names_as_csv(new_names, csv_filename)
    


# Driver Code 
if __name__ == '__main__':
    main()


