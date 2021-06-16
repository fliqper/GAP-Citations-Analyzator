Instructions for use:
This is the web-scraping tool.
We have two Python files:
 + Scrapings.py this script is ready and set with 'GapBibMR.csv' as input and all you need to do is enter `python3 Scrapings.py` in your python environment.
 + Scrag.py takes one argument so if you enter `Scrag.py local` it will use `test_input.csv` and our test URL, and if you enter `Scrag.py remote` it will work the same as Scrapings.py using the 'GapBibMR.csv' for input and the MathSciNet URL.
 
In order for either of the scripts to work the following conditions need to be met:
 + it needs to be run on the authorised server 'kovacs'
 + the input 'GapBibMR.csv' file needs to be placed in the same directory with Scrapings.py or Scrag.py
 + Python version 3 or higher is needed.
 
 Both scripts require the following libraries Pandas, Regex, BeautifulSoup4, Requests, Itertools,
 + if you need to install some of them please enter the following commands in your Python environment:
     - pip install bs4
     - pip install regex
     - pip install requests
     - pip install pandas
     - pip install more-itertools


