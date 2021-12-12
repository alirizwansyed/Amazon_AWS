import pandas as pd
import os
import glob
import math

no_of_files = 7

input_split_file = r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_After_BadKeywords20211212-095613PM.csv"
output_split_file = os.path.splitext(input_split_file)[0]
input_merge_file= r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_After_BadKeywords20211212-095613PM_1.csv"
output_merge_file = (os.path.splitext(input_merge_file)[0])[:-len(str(no_of_files))]

def csv_split():
    print("File Split Started")
    df = pd.read_csv(input_split_file) # reading file
    start_row = 0
    end_row = math.floor(len(df)/no_of_files)
    rows_per_file = end_row
    i=1
    # low = 0 # Initial Lower Limit
    # high = 1000 # Initial Higher Limit
    while(end_row < len(df)):
        df_new = df[start_row:end_row] # subsetting DataFrame based on index
        start_row = end_row #changing lower limit
        end_row = end_row + rows_per_file # givig uper limit with increment of 1000
        df_new.to_csv(output_split_file+"_"+str(i)+".csv", index=False) # output file 
        i=i+1
        print("Files Split complete")

def csv_merge():
    print("Files Merge Started")
    # merging the files
    joined_files = output_merge_file+"*"+".csv"
    # A list of all joined files is returned
    joined_list = glob.glob(joined_files)
    # Finally, the files are joined
    df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
    # print(df)
    df.to_csv(output_merge_file+"_2.csv", index=False) # output file 
    print("Files Merge complete")

# csv_split()
csv_merge()