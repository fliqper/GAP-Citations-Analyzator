#!/usr/bin/env python
# coding: utf-8

# Full scraping workflow using Requests, BeautifulSoup combined with Regex

# First we call the libraries needed.

import sys
import time
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import itertools

# running_mode will be difined by an argument when running the script /remote or local/

running_mode = sys.argv[1]

if running_mode == 'remote':

	# We load the input .csv file containing the MR number and conver it to a Python list.

	input_data = pd.read_csv('GapBibMR.csv', dtype = 'str')
	type_change = input_data.values.tolist()
	mrn_numbers_only = list(itertools.chain(*type_change))

	# Now we need to verify they are 7 digit long numbers, before we continue.
	# In order to make sure none of the old-style MR numbers remain.

	mrn = [] # list of all good MR numbers, made up from exactly 7 digits, that we will search for citations
	non_standard_mrn = [] # list of non-standard MR numbers

	for i in range(len(mrn_numbers_only)):
		if (mrn_numbers_only[i].isnumeric() and len(mrn_numbers_only[i]) == 7):
			each_mrn = ('MR' + mrn_numbers_only[i])
			mrn.append(each_mrn)
		else:
			non_standard_mrn.append(mrn_numbers_only[i])

	print('Total input elements:')
	print(len(mrn_numbers_only))
	print('Number of non-standart elements isolated for updating:')
	print(len(non_standard_mrn))
	print('Number of standard MR elements, that will be searched for GAP citations:')
	print(len(mrn))

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
		return re.compile(regex, flags=re.DOTALL | re.IGNORECASE)


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
	print('Initiate GAP citation scan...')

	base_URL = "http://www.ams.org/mathscinet/search/publications.html?fmt=html&pg1=MR&s1="
	all_matches = []
	review_later = []
	actual_scrapes = []
	for i in range(len(mrn)):
		url = (base_URL + mrn[i])
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		match = (find_by_text(soup, 'GAP', 'li', mrn[i]))
		if match is None:
			review_later.append(mrn[i])
		else:
			all_matches.append(match)
			actual_scrapes.append(mrn[i])
		# the following print statements allow user to track progress.
		print('Working on page:')
		print(i)
		print('from a total of:')
		print(len(mrn))
		print('Citations found in page:')
		print(match)
		print(' ') # to skip a line for better readability
		time.sleep(5) # adding 5 seconds rest interval between iterations  to avoid overloading the source website and also not to risk activating their security sentinel algorithms

	print('Finished GAP citation scan...')

elif running_mode == 'local':
	# We load the input .csv file containing the MR number and conver it to a Python list.

	input_test = pd.read_csv('test_input.csv')
	type_change = input_test.values.tolist()
	mrn_numbers_only = list(itertools.chain(*type_change))
	type(mrn_numbers_only)
	
	# Now we need to verify they are 7 digit long numbers, before we continue.
	# In order to make sure none of the old-style MR numbers remain.

	mrn = [] # list of all good MR numbers, made up from exactly 7 digits, that we will search for citations
	non_standard_mrn = [] # list of non-standard MR numbers

	for i in range(len(mrn_numbers_only)):
		#if (mrn_numbers_only[i].isnumeric() and len(mrn_numbers_only[i]) == 7):
		each_mrn = ('MR' + str(mrn_numbers_only[i]))
		mrn.append(each_mrn)
		#else:
	#		non_standard_mrn.append(mrn_numbers_only[i])

	print('Total input elements:')
	print(len(mrn_numbers_only))
	print('Number of non-standart elements isolated for updating:')
	print(len(non_standard_mrn))
	print('Number of standard MR elements, that will be searched for GAP citations:')
	print(len(mrn))

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
	print('Initiate GAP citation scan...')

	base_URL = "D:\\"
	
	all_matches = []
	review_later = []
	actual_scrapes = []
	
	for i in range(len(mrn)):
		url = (base_URL + mrn[i] + '.html')
		page = open(url, encoding="utf8") 
		soup = BeautifulSoup(page, 'html.parser')
		match = (find_by_text(soup, 'GAP', 'li', mrn[i]))
		if match is None:
			review_later.append(mrn[i])
		else:
			all_matches.append(match)
			actual_scrapes.append(mrn[i])
		# the following print statements allow user to track progress.
		print('Working on page:')
		print(i)
		print('from a total of:')
		print(len(mrn))
		print('Citations found in page:')
		print(match)
		print(' ') # to skip a line for better readability
		#time.sleep(5) # adding 5 seconds rest interval between iterations  to avoid overloading the source website and also not to risk activating their security sentinel algorithms

	print('Finished GAP citation scan...')

# Before we continue we export the list of pages for further review as .CSV
further_review = pd.DataFrame(review_later)
further_review.to_csv('review.csv', index=False, encoding='utf-8')

# Some of the test HTMLs did not contain the word GAP and they returned NoneType elements. 
# Using the following list comprehension we will remove them before we continue.

all_matches = [i for i in all_matches if i is not None]

# The resukt is a list of lists, one list for each MR number, but some pages contain several GAP citations.
# Therefore, we will convert our result to a list of strings, so we have alternating strings of MR number followed by its citation.

joined = list(itertools.chain(*all_matches))

# Finally we will strip each string to remoe any remaining HTML markup, most of them are fine but we need to be sure.

final = []
for i in range(len(joined)):
    clean = (joined[i].strip())
    final.append(clean)

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
print('Total number of results is: ' + str(len(joined)) + ' and they are stored in the file \'output.csv\'')
#print('Below is the list of all results.')
#print(final_df)

# The resultung Pandas Data-frame has two columns. 
# Now we can export it to a .CSV file which will be taken over by the next Jupyter Notebook in our pipeline.

final_df.to_csv('output.csv', index=False, encoding='utf-8')
