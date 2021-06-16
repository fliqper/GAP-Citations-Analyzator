#!/usr/bin/env python
# coding: utf-8

# Full scraping workflow using Requests, BeautifulSoup combined with Regex

# First we call the libraries needed.

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import itertools

# We load the input .csv file containing the MR number and conver it to a Python list.

input_test = pd.read_csv('test_input.csv')
mrn = (input_test['0'].tolist())
print(mrn)

# We define two functions used together to find all GAP citations by HTMl element and text contained inside it. 
# They can be re-used in future we-scraping projects too.

MATCH_ALL = r'.*'

def like(string):
    """
    Return a compiled regular expression that matches the given
    string with any prefix and postfix, e.g. if string = "hello",
    the returned regex matches r".*hello.*"
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(regex, flags=re.DOTALL)


def find_by_text(soup, text, tag, mrn, **kwargs):
    """
    Find the tag in soup that matches all provided kwargs, and contains the
    text.

    If no match is found, raise ValueError.
    """
    empty = 1
    elements = soup.find_all(tag, **kwargs)
    matches = []
    for element in elements:
        if element.find(text=like(text)):
            matches.append(mrn + ':')
            matches.append(element.text.strip())
    if len(matches) == 0:
        pass
    else:
        return matches

# Now we use both functions in a for loop to search all pages specified by MR number in the input .csv file. 
# All the matching results are joined in a list.

base_URL = "https://sis1.host.cs.st-andrews.ac.uk/GAP/"
all_matches = []

for i in range(len(mrn)):
    url = (base_URL + mrn[i] + '.html')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    match = (find_by_text(soup, 'GAP', 'li', mrn[i]))
    all_matches.append(match)

# Some of the test HTMLs did not contain the word GAP and they returned NoneType elements. 
# Using the following list comprehension we will remove them before we continue.

all_matches = [i for i in all_matches if i is not None]

print(type(match))
print(type(all_matches))
print('Results count is:', len(all_matches))

# The resukt is a list of lists, one list for each MR number, but some pages contain several GAP citations.
# Therefore, we will convert our result to a list of strings, so we have alternating strings of MR number followed by its citation.
joined = list(itertools.chain(*all_matches))

print(type(joined))
print(type(joined[1]))
print('Now the Results count is:', len(joined), ' which confirms that our program also catches GAP Packages citation as separate results.')

# Finally we will strip each string to remoe any remaining HTML markup, most of them are fine but we need to be sure.

final = []
for i in range(len(joined)):
    clean = (joined[i].strip())
    final.append(clean)
final
print(final)

# Converting our data to Pandas dataframe for further analysis

df=pd.DataFrame(final)
df

# Some MR numbers contain more than one GAP citations which produces extra columns. 
# We need to take every odd element from the whole data and assign it to separate row in one 'MR' column. 
# And then take every even element containing the corresponding citation and join it to its MR number in a second column called 'Citation'.

check = df.index%2==0  #checking if the index is even because the values are in consicutive order
final_df = pd.DataFrame([df.loc[check, 0].str.strip(':').tolist(), # taking every odd element which is MR number
                         df.loc[~check, 0].tolist()], # taking every even element which is Citation
                         index=['MR','Citation']).T # assigning the corresponding value names to each column

print(final_df)

# The resultung Pandas Data-frame has two columns. 
# Now we can export it to a .CSV file which will be taken over by the next Jupyter Notebook in our pipeline.

final_df.to_csv('test_output.csv', index=False, encoding='utf-8')
