#!/usr/bin/env python
# coding: utf-8

# ### Full scraping workflow using Requests, BeautifulSoup combined with Regex

# First we call the libraries needed.

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import itertools


# We load the input .csv file containing the MR number and conver it to a Python ```list```.

# In[2]:


input_test = pd.read_csv('test_input.csv')
mrn = (input_test['0'].tolist())
print(mrn)


# We define two functions used together to find all GAP citations by HTMl element and text contained inside it. They can be re-used in future we-scraping projects too.

# In[12]:


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


# In[13]:


base_URL = "https://sis1.host.cs.st-andrews.ac.uk/GAP/"
#mrn = ["MR3", "MR4044696", "MR2900886", "MR3169623", "MR4180136", "MR4044697", "MR7", "MR5", "MR1111111", "MR11"]
url_list = []
all_matches = []

for i in range(len(mrn)):
    url = (base_URL + mrn[i] + '.html')
    url_list.append(url) #for records keeping only, not really needed 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    match = (find_by_text(soup, 'GAP', 'li', mrn[i]))
    all_matches.append(match)
    
all_matches


# In[14]:


print(type(all_matches[0]))


# Some of the test HTMLs did not contain the word GAP and they returned NoneType elements. Using the following list comprehension we will remove them from the results before we continue.

# In[15]:


all_matches = [i for i in all_matches if i is not None]
all_matches


# In[16]:


print(type(match))
print(type(all_matches))
print('Results count is:', len(all_matches))
print(all_matches[2])


# In[19]:


joined = list(itertools.chain(*all_matches))
joined


# In[20]:


print(joined[3])
print(type(joined))
print(type(joined[1]))
print('Now the Results count is:', len(joined), ' which confirms that our program also catches GAP Packages citation as separate results.')


# In[24]:


final = []
for i in range(len(joined)):
    clean = (joined[i].strip())
    final.append(clean)
final


# ### Converting our data to Pandas dataframe for further analysis

# In[80]:


df=pd.DataFrame(final)
df


# Some MR numbers contain more than one GAP citations which produces extra columns. We need to take every odd element from the whole data and assign it to separate row in one 'MR' column. And then take every even element containing the corresponding citation and join it to its MR number in a second column called 'Citation'.

# In[98]:


check = df.index%2==0  #checking if the index is even because the values are in consicutive order
separated = pd.DataFrame([df.loc[check, 0].str.strip(':').tolist(), # taking every odd element which is MR number
                         df.loc[~check, 0].tolist()], # taking every even element which is Citation
                         index=['MR','Citation']).T # assigning the corresponding value names to each column


# In[99]:


separated


# The resultung Pandas Data-frame has two columns. Now we can export it to a .CSV file which will be taken over by the next Jupyter Notebook in our pipeline.

# In[101]:


separated.to_csv('output.csv', index=False, encoding='utf-8')


# In[ ]:




