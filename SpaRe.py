"""
The program locates Spatial Relation (SpaRe) in a text and creates a
visualisation of the frequency distribution of Spatial Indicators.


Text used: AliceCH1.txt
    The first chapter from Alice's Adventures in Wonderland by Lewis Carroll.
    The text is from Project Gutenberg at https://www.gutenberg.org/ebooks/11. 
    See 'ParatextAlice.txt' for further information and license.

Excel file: AliceSpReCh1.xlsx
    The Excel file AliceSpReCh1.xlsx contains snippets from the text
    that indicate SpaRe. For the purposes of this study SpaRe was defined as
    instances where Spatial Indicators (SpIns) occur and are evidently linked
    to space and place. The data was cleaned manually.

SpIns:
    back, across, against, along, around, at, behind, below, besides, by, down,
    from, in, into, near, of, off, on, out, outside, over, through, to,
    towards, under, underneath, up, here, there

Linguistics and Semantics of SpaRe:
    The instances of SpIns that were judged as referring to SpaRe are
    prepositions that are part of prepositional phrases or phrasal verbs.
    Additionally, the demonstratives 'here' and 'there' were also considered as
    referring to SpaRe.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math


def clean_text(text):
    """
    Cleans the input text by removing non-alphanumeric characters
    except spaces and hyphens and replaces multiple successive spaces with
    a single space. Apostrophes are replaced with blank space.
    Args:
        text (str): The text file to be cleaned.
    Returns:
        str: Cleaned text as a single string.
    """
    with open(text) as file:
        text_as_string = file.read().replace('\n', ' ')

    # remove all non-alphanumeric characters from string except for blank space
    alnum_and_space = ''
    for letter in text_as_string:
        if letter.isalpha() or letter == ' ' or letter == '-':
            alnum_and_space += letter
        elif letter == '’':     # Replace apostrophes with blank space
            alnum_and_space += ' '

    # Remove multiple successive spaces
    alnum_and_single_space = ''
    for index in range(len(alnum_and_space)-1):
        if alnum_and_space[index] == ' ':
            if not alnum_and_space[index+1] == ' ':
                alnum_and_single_space += alnum_and_space[index]
        else:
            alnum_and_single_space += alnum_and_space[index]

    return alnum_and_single_space


# transforms Excel sheet with snippets from text into list
def excel_into_list(filename, sheet, column):
    """
    Converts a specified column from an Excel sheet into a Python list.
    Args:
        filename (str): Path to the Excel file.
        sheet (str): Name of the sheet to read from.
        column (str): Column name to convert into a list.

    Returns:
        list: List of values from the specified column.
    """
    df = pd.read_excel(filename, sheet_name=sheet)
    column_list = df[column].tolist()
    return column_list



# locates individual spatial relations in text
# snippets is a list consisting of five-word string elements that occur before
# a spatial indicator (SpIn)
# SpIns: back, across, along, at, behind, by, down, from, in,
# into, near, of, off, on, out, through, to, under, underneath, up, here, there

def find_SpaRe(text, snippets):
    """
    Locates instances of Spatial Relations (SpaRe) in the text based on
    provided snippets.
    Args:
        text (str): The cleaned text to search.
        snippets (list): List of 5-word string elements that occur before
        a spatial indicator (SpIn).
        SpIns: back, across, along, at, behind, by, down, from, in, into, near,
        of, off, on, out, through, to, under, underneath, up, here, there

    Returns:
        list: Indices of spatial indicators (SpIns) in the text.
    """
    # Dictionary to store snippet start index and length
    location_and_length = {}
    snippet_indices = []

    for x in range(len(snippets)-1):
        index = text.find(snippets[x])  # Find index of snippet
        snippet_indices.append(index)
        snippet_length = len(snippets[x])
        # Add location of snippet (index of first char) and length to dict
        location_and_length.update({index : snippet_length})

    # Calculate the location of SpIns based on snippet indices and lengths
    SpIn_location = []     # List of locations (indices) of SpIns
    for x in location_and_length:
        # location of SpIn is one char after each snippet
        index = x + location_and_length[x] + 1
        SpIn_location.append(index)

    return SpIn_location


def freq_SpIn(SpIn_location, text, nr_of_chunks):
    """
    Calculates the frequency distribution of Spatial Indicators (SpIns) across
    equally divided chunks of text.
    Args:
        SpIn_location (list): Indices of spatial indicators in the text.
        text (str): The cleaned text.
        nr_of_chunks (int): Number of chunks to divide the text into.

    Returns:
        dict: Dictionary mapping chunk number to the frequency of SpIns in
        that chunk.
    """
    densities = {}
    # Length of each chunk
    chunk_length = math.ceil(len(text)/nr_of_chunks)    # e.g. 10792 / 50 = 216

    # Iterate over chunks and count SpIns in each chunk
    x = 0
    for chunk in range(1, nr_of_chunks + 1):
        if (chunk == 1):
            end = (chunk_length * chunk)
        else:
            # next chunk needs to begin 1 char after the end of prior chunk,
            # hence + x where x is a variable that increases by 1 at each
            # iteration
            end = (chunk_length * chunk) + x
        start = end - chunk_length
        x += 1
        #print('chunk:', chunk)    # test output
        #print('start:', start)    # test output
        #print('end:', end)        # test output

        count = 0
        # Dictionary mapping chunk number to the frequency of SpIns in
        # that chunk.
        # If no SpIns in chunk, then frequency = 0
        densities.update({chunk: 0})
        for SpIn_index in range(len(SpIn_location)):
            if start <= SpIn_location[SpIn_index] <= end:
                count += 1  # increase count when SpIn occurs
                densities.update({chunk : count})

    return densities


def draw_plot(densities):
    """
    Creates a bar plot showing the distribution of Spatial Indicators (SpIns)
    across text chunks.
    Args:
        densities (dict): Dictionary mapping chunk number to SpIn frequency.
    """
    x_chunks = list(densities.keys())
    y_freq = list(densities.values())

    # create bar chart
    plt.bar(x_chunks, y_freq)
    plt.title('Frequency distribution of Spatial Indicators', fontsize=14)
    plt.ylabel('Frequency of SpIns per segment', fontsize=10)
    plt.xlabel('Total characters in text divided into 50 segments',
               fontsize=10)
    plt.show()


def main():
    """
      Main function to execute the SpaRe analysis and visualisation.
    """
    og_text = 'AliceCH1.txt'
    # Clean text to prepare data for further processing
    cleaned_text = clean_text(og_text)

    # Read snippets from Excel sheet and save into list
    SpaRe_list = excel_into_list('AliceSpReCh1.xlsx', 'finalList',
                                 'context [5:]')

    # Find SpIn locations
    SpIn_location = find_SpaRe(cleaned_text, SpaRe_list)

    nr_of_chunks = 50
    # Calculate frequencies
    densities = freq_SpIn(SpIn_location, cleaned_text, nr_of_chunks)
    draw_plot(densities)    # Visualize the results


if __name__ == "__main__":
    main()
