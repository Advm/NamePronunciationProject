import sys
import pandas as pd

def take_input(func):
    """
    take_input checks if there was a filename provided on the command line.
    If so, it calls read_file with the provided cmd line argument.
    Otherwise, it begins manual entry of words/names.
    Each time a word is entered, it is passed to the provided func
    This continues until the user enters nothing.

    Params: func (function) -- function that the input is passed to
    Returns: Nothing
    """
    # Manual Input
    if len(sys.argv) < 2:
        while True:
            user_in = input("Please enter a word/name "\
                            "(Enter nothing to exit): ")
            if user_in == "":
                print("Goodbye!")
                break
            else:
                func(user_in)
    # File input
    else:
        read_file(sys.argv[1], func)

def read_file(filename, func):
    """
    Function reads filename as a csv into a pandas dataframe, then calls the
    provided func function with the dataframe as a parameter

    Params: filename (str) -- filename/path to read in as csv
            func (function) -- function that is called on the dataframe produced
    Returns: Nothing

    """
    # encoding ="UTF-8" needed for IPA chars
    in_file = open(filename, encoding="UTF-8")
    dataframe = pd.read_csv(in_file, sep=",", names=["Word", "IPA"])
    func(dataframe)

def write_dataframe(filename, dataframe):
    """
    Function is a simple wrapper for pandas' DataFrame.to_csv function.
    Will probably be useful enventually when more advanced ui is made

    Params: filename (str) -- filename/path to write dataframe into
            dataframe (pd.DataFrame) -- data to write to file
    Returns: Nothing
    """
    dataframe.to_csv(filename, header=["Word","Pronuncation Rating"])



def main():
    """
    Main just calls take input with print as the function
    """
    take_input(print)

if __name__ == "__main__":
    main()
