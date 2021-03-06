	Project: GAP Citations Analyzator

The GAP citations dataset was assembled using the MathSciNet database.
We would like to express our gratitude to the American Mathematical Society for giving us
such opportunity.

Our software consists of 3 parts, the first is a web-scraper in the form of Python script
file â.pyâ, the other two parts are Jupyter Notebooks.

If you cannot run the code for various reasons, you can still study the project using the 
`Auxiliary` folder. It contains both Jupyter Notebooks as PDF files and the 3 maps we created
as HTML files.

	Part 1. Instructions for use for the web-scraping tool. 
	
Location: Scraper.py is located in the `code` folder.  

Input: CSV file containing MR numbers, or any other list of suffixes to be combined with the URL 
base. Currently the input for local mode is `test-input.csv` and for remote mode `GapBibMR.csv`. 
 
Output /in remote mode/: two CSV files: 1. `output.csv` whcih once it run successfully we copied
and renamed to `gap_citations_corpus.csv` to be used by the next module in the
pipeline - Data Prep Module Jupyter notebook 
2. `review.csv` which contains any anomalies, it was copied and renamed 
to  `no_citation_text.csv` in the notebooks folder to be loaded by the Data Prep Module.   

It takes one argument to specify mode of operation â local or remote. All you need to do is run
the script using one of the two arguments and it will retrieve information from the web as per
your input, then produce output CSV files to be processed and analysed using the next two parts
of the software.  
-if you enter `python Scraper.py local` in your python environment it will use test_input.csv and our test URL which is `D:\`,  
-or if you enter `python Scraper.py remote` it will use the GapBibMR.csv for input and the MathSciNet website URL. 

Reusability: 
If you need to use the tool for retrieving information from another website, you will need to
update the base URL, input file and the scraping loop, depending on the element where your target
information is located in the HTML.  

Prerequisites:  for the scripts to work the following conditions need to be met:  

	o	Python version 3 or higher is needed - https://www.python.org/downloads/  
	Video: https://www.youtube.com/watch?v=rVb1TqqbPj0  
	 
	o	Scraper.py remote needs to be run on the authorised server 'kovacs' so it can access the
	MathSciNet database  

	o	both input CSV files need to be placed in the same directory with or Scraper.py otherwise
	the file-path in the code should be updated  
	o	The tool requires the following libraries: Pandas, Regex, BeautifulSoup4, Requests, itertools,
	sys, time.
  
In case you need to install some or all of them please use the `requirements.txt` in the general
project directory.


	Part 2.	Instructions for using the second part Data Prep Module.ipynb 
	
Location: `notebooks` folder.  

Input: one BIB file `gap-publishednicer.bib` downloaded from GAP website and two CSV files
produced by `Part 1`:`gap_citations_corpus.csv` and `no_citation_text.csv`. 
  
Output: 3 CSV files: `full.csv`, `gap.csv` and `pac.csv`.  

Prerequisites:  
If you do not have Jupyter Notebook installed, this official documentation guide will 
help: https://test-jupyter.readthedocs.io/en/latest/install.html . 
As prerequisites you need the latest version of Python and the following libraries:
	-bibtexparser 
	-itertools
	-requests
	-re
	-matplotlib
	-pandas
	-BeautifulSoup
	-Numpy

Providing the default input provided with the project is used, you can run all cells and the
tool will prepare the data for analysis. 

In case input was modified, then the whole code should be revised to match the new data column
names.  

It will output 3 CSV files, one containing the whole data `merged_df` and two subsets containing
filtered data for pure GAP citations `gap_df` or for GAP Packages only `pac_df`.  



	Part 3. Instructions for using the third part Data Analysis and Visualisation.ipynb  

Location: `notebooks` folder.  

Input: 3 CSV files produced by `Part 2`: `full.csv`, `gap.csv` and `pac.csv`.  
Output: No files, visualisations and analysis viewed directly in the notebook along with the code.  

Prerequisites: They are the same as for Part 2, but we use additional libraries here: matplotlib,
json, os, folium, branca, folium.features, __future__, ipywidgets, cufflinks.

Implementation:
To use the tool simply open the file Data Analysis and Visualisation.ipynb using your Jupyter
Notebook in your browser.
If the default input was used and no modifications were made to the first two parts of the
software pipeline, then you can run the whole notebook. It will then display all visualisations
and tables, which you can study by scrolling your mouse. There are interactive visualisations 
which will change as you update their parameters using the drop-down elements. 
 
Reusability:  
In case you modified the first two parts of the software, you will need to edit most of the code 
in this notebook to adjust it to the new incoming data, mainly you need t make sure column names 
in your data and your code match, and datatypes of the columns must be appropriate for the 
performed operations. For instance, we can only take the mean of a column which contains only 
numerical cells.