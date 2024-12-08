# CODE TO CONVERT MULTIPLE FILES
# RUN AS ADMINISTRATOR OR IT WON'T BE ABLE TO ACCESS SOME FILES

# Written by Joey Ungerleider
###############################################################################

import re      # REGEX
import shutil  # shutil
import os      # operating system
import csv     # CSV

###############################################################################
# Function to replace certain text with other text
# Inputs:  original_file_path -- directory of the file you want to copy
#          original_file_path -- path of where to copy the file to
def copy_file(original_file_path, new_file_path):
    shutil.copyfile(original_file_path, new_file_path)

# Function to replace certain text with other text
# Inputs:  filepath -- directory of the file you want to manipulate
#          from_    -- what text(s) to replace
#          to_      -- what to replace the text with
def replace(filepath, from_, to_):
    file = open(filepath,'r+')
    text = file.read()
    pattern = from_
    splitted_text = re.split(pattern,text)
    modified_text = to_.join(splitted_text)
    with open(filepath, 'w') as file:
        file.write(modified_text)

# Function to delete a SINGLE line
# Inputs:  filepath    -- directory of the file you want to manipulate
#          line_number -- which line you want to delete; first line is 1!!!
def deleteline(filepath, line_number):
    file = open(filepath,'r+')
    lines = file.readlines()
    numlines = len(lines)
    if 0 < line_number <= numlines:
        del lines[line_number - 1]
    newfile = open(filepath, 'w')
    newfile.writelines(lines)
    
    newfile = open(filepath, 'r+')
    lines = newfile.readlines()
    numlines = len(lines)
    
    # print("Old # Lines:",numlines)
    # print("New # Lines:",numlines)
    
# Function to delete MANY lines
# Inputs:  filepath   -- directory of the file you want to manipulate
#          first_line -- the first line to delete (inclusive), to...
#          last_line  -- the last line to delete (inclusive)
def deletemultlines(filepath, first_line, last_line):
    x = (last_line - first_line + 1)
    for i in range(x):
        deleteline(filepath, first_line)

# Function count how many lines until a certain character is detected
# Inputs:  filepath  -- directory of the file you want to manipulate
#          character -- the character you want to detect
def count_lines_until_character(filepath, character):
    line_count = 0
    with open(filepath, 'r') as file:
        for line in file:
            line_count += 1
            if character in line:
                break
    return line_count

# Function count how many lines until a certain character is detected
# Inputs:  file1_path        -- path of 1st file you want to combine with...
#          file2_path        -- path of 2nd file you want to combine
#          output_file_path  -- directory where the output will go
def combine_files(file1_path, file2_path, output_file_path):
    # Read content of file1
    with open(file1_path, 'r') as file1:
        file1_content = file1.read()

    # Read content of file2
    with open(file2_path, 'r') as file2:
        file2_content = file2.read()

    # Write combined content to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(file1_content)
        output_file.write(file2_content)
          
# Function Create a name of file with a certain suffix after its name
# Inputs:  filepath   -- directory of the file you want to manipulate
def create_copy_name(filepath, suffix):
    # Split the original directory path into its base name and extension
    base_name, extension = os.path.splitext(filepath)

    # Append the suffix to the base name
    new_base_name = base_name + suffix

    # Reconstruct the new directory path with the original extension (if present)
    new_directory_path = new_base_name + extension

    # Copy the original directory to the new location with the new name
    #shutil.copy(filepath, new_directory_path)

    return new_directory_path


# Function Create a name of file with a certain file extension
# Inputs:  filepath        -- directory of the file you want to manipulate
# Inputs:  new_extension   -- the new file extension
def change_file_extension(filepath, new_extension):
    # Split the file path to get the file name and its extension
    file_name, old_extension = os.path.splitext(filepath)

    # Construct the new file path with the desired extension
    new_file_path = file_name + new_extension

    # Rename the file
    os.rename(filepath, new_file_path)

    return new_file_path

# Function count how many lines until a certain character is detected
# Inputs:  txt_file_path -- input path of txt file
#          csv_file_path -- output path of a csv file
def txt_to_csv(txt_file_path, csv_file_path):
    # Read the comma-separated values from the text file
    with open(txt_file_path, 'r') as txt_file:
        lines = txt_file.readlines()

    # Write the data into a CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for line in lines:
            csv_writer.writerow(line.strip().split(','))
###############################################################################

def single_file_process(inputpath):
    
    # Define a file path
    original_file_path = inputpath
    # Define a copy file path
    copy_file_path = create_copy_name(inputpath, '_copy')
    
    # Create a copy of the original file:
    copy_file(inputpath, copy_file_path)
    
    topfilepath = original_file_path
    bottomfilepath = copy_file_path

    # Process the information headers (the top half) from each .txt file into .csv format
    
    # Count how many info lines the txt file has
    line_count = count_lines_until_character(topfilepath, "*")
    print("Number of lines until *** bar:",line_count)
    
    # Delete everything after the top info
    deletemultlines(topfilepath, (line_count - 5), 800)    # KEEP THIS COMMENTED OUT WHEN TESTING
    
    # replace ": " with a comma to separate headers from info
    replace(topfilepath, ": ", ",")

    # Process the data (the bottom half) from each .txt file into .csv format
    
    # Count how many info lines the txt file has
    line_count = count_lines_until_character(bottomfilepath, "*")
    print("Number of lines until *** bar:",line_count)
    
    # Delete lines 1 through the line where the *** bar is:
    deletemultlines(bottomfilepath, 1, line_count)    # KEEP THIS COMMENTED OUT WHEN TESTING
    
    # replace 3 spaces with 2 spaces
    replace(bottomfilepath, "   ", "  ")
    # replace 2 spaces with 1 space
    replace(bottomfilepath, "  ", " ")
    # replace 1 spaces with a comma
    replace(bottomfilepath, " ", ",")
    
    # replace 3 commas with 2 commas
    replace(bottomfilepath, ",,,", ",,")
    # replace 2 commas with 1 comma
    replace(bottomfilepath, ",,", ",")

    # Combine our two (top and bottom) processed files into a single .csv file 
    
    # Write the top and bottom parts of our txt file to one single file
    comb_file_path = create_copy_name(inputpath, '_CSV')
    combine_files(topfilepath, bottomfilepath, comb_file_path)
    
    # Change file extension from '.txt' to '.csv'
    csv_file_path = change_file_extension(comb_file_path, '.csv')
    
    # Print where the final csv is located
    print("The final CSV file is located at: ",csv_file_path)
    
###############################################################################


# Loop through each txt file in a folder and convert it to csv

def mult_file_process(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter out only the text files
    txt_files = [file for file in files if file.endswith('.txt')]

    # Process each text file
    for txt_file in txt_files:
        # Construct the full path to the text file
        txt_file_path = os.path.join(folder_path, txt_file)
        
        # process each file
        single_file_process(txt_file_path)
        
        # For demonstration, let's print the file name
        print("Processing:", txt_file_path)
        
    print("Done processing all files!")

###############################################################################

# REPLACE THIS WITH THE FOLDER YOU WANT TO RUN THROUGH
mult_file_process('C:\Program Files\Spyder\RocketNoiseDataBase\FALCONHEAVY_ARABSAT6A-LAUNCHNOISE')

