import re, pandas as pd, os

"""
========= Required Software =========
Anaconda3 (running python 3.7.6), may not be compatible with previous versions

========= INTENT OF THIS CODE =========
This code should be used to grab the longest wire length from docs.
It can run MORE THAN ONE document at a time.

========= USER GUIDE =========
1. From file sharing area, grab the documents as a PDF
2. Open it in any PDF reader software. 
3. Use the keyboard shortcut "ctrl+a" to select all text values of the doc
4. Open Notepad or Notepad++ or any other TEXT editing software.
5. Paste values from doc to text editing file.
6. Save the text document as the name in the same area as this code.
7. Run the code

"""

WORKING_FOLDER = "./<name_of_working_folder>"
#WORKING_FOLDER = "."

os.chdir(WORKING_FOLDER)
input_file_list = []
for file in os.listdir():
    if file.split(".")[1] == "txt":
        input_file_list.append(file)


#=============================================================================#
def longestCableLength(input_file):
    output_file="longestCableLength_" + input_file.split(".")[0] + ".csv"
    
    with open(input_file, "r", encoding="utf8") as infile:
        lines = infile.readlines()
    
    # list comprehension to grab lines in the input_file that have a match for search_pattern
    search_pattern = r'W\d{4}-\d{3}'
    regex_filtered_lines = [line.strip() for line in lines if re.search(search_pattern, line)] 
    
    # only pull out lines with 11 columns and then remove duplicate lines
    lines_with_eleven_columns = []
    for line in regex_filtered_lines:
        columns = line.split()
        if len(columns) in [10, 11]:
            mod_line = line.replace(" ", ",")
            lines_with_eleven_columns.append(mod_line)        
    unique_lines = list(set(lines_with_eleven_columns)) 
    
    # Turn unique_list to a list of lists
    unique_lines2 = []
    for line in unique_lines:
        unique_lines2.append(line.split(","))
    
    # Grab unique wire names in the file
        # Indexing needs to be negative, lines of interest can either be 10 or 11 columns
    wire_names = []
    for line in unique_lines2:
        wire_names.append(line[-6])
    unique_wires = list(set(wire_names)) 
    
    # create a dictionary to fill later
    wire_dict = {wire:[] for wire in unique_wires}
    
    # fill wire_dict with gauge, EMI circuit class, and length (but also only grab longest length per wire name)
    for line in unique_lines2:
        if line[-6] in unique_wires:
            try: # first go around will cause issues since wire_dict is not filled
                if wire_dict[line[-6]][2] < line[-1]:
                    wire_dict[line[-6]] = [line[-5], line[-4], line[-1]] 
            except IndexError:
                wire_dict[line[-6]] = [line[-5], line[-4], line[-1]]
            
    # output to file
    wire_df = pd.DataFrame.from_dict(wire_dict, orient="index", columns =["Gauge","EMI Wire Class","Length"])
    wire_df = wire_df.sort_index()
    wire_df.to_csv(output_file)       
#=============================================================================#

for file in input_file_list:
    longestCableLength(file)