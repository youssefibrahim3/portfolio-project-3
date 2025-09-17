# user_csv.py
# ENDG 233 F24
# STUDENT NAME(S): Youssef Ibrahim, David Caranay
# GROUP NAME: T1
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.

def read_csv(filename, include_headers):
    """Will read a .csv file and convert it to a numpy array.
    
    Parameters:
        filename (str): the file path
        include_headers (bool): if true first line from the .csv is included, if false first line from .csv file is not included

    Returns:
        data (2D list): The data from the .csv file in a 2D numpy array
    """
    file = open(filename, "r") # Reads the .csv file.
    data = []
    # Return a 2D list.
    for line in file:
        # Creating a list of entries, split by commas
        split_line = line.split(",")   
        # Making numbers into floats instead of strings
        for i in range(len(split_line)):
            # Checking if the string contains a float
            float_check = split_line[i].replace(".","")
            float_check = float_check.replace("\n","")

            # After removing all periods and \n from the string, check if it's a number
            if float_check.isdecimal():
                split_line[i] = float(split_line[i])
                round(split_line[i], 2) # Round float to two decimal places
        data += [split_line]
    
    if not include_headers:
        del data[0] # Deletes the headers.

    file.close() # Close file.
    return data

def write_csv(filename, data, overwrite):
    """Will overwrite/append data in a .csv file.
    
    Parameters:
        filename (str): File path of desired file
        data (string): Data to be written to the file
        overwrite (bool): if True overwrites data in the .csv, if False appends data to .csv
    """
    if overwrite:
        file = open(filename, "w") # Opens file to overwrite data in the .csv file.
    else:
        file = open(filename, "a") # Opens file to add additional data to the .csv file.
    file.write(data) # Edits the data and saves it.
    file.close() # Close file.