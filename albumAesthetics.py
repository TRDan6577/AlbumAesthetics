from bs4 import BeautifulSoup
import mechanize
import re

br = mechanize.Browser()
br.set_handle_robots(False) # Be mean and ignore the site's request to not use robots
br.addheaders = [('User-Agent', 'Mozilla')] # pretend we're a browser
html = br.open("https://www.google.com/search?q=this+is+a+test&safe=off&tbm=isch")

# prepare some delicious soup
soup = BeautifulSoup(html.read(), 'html.parser')

# URLs for images searches on google:
# https://www.google.com/search?q=my+search+terms+here&safe=off&tbm=isch
# disected....                   |   1                | 2      | 3
# 1) Search result separated by spaces
# 2) Turn off safe search for all results
# 3) Set the type of search to an image search

# Then in print(soup.prettify()), look for the a href. Get rid of the 
# '/url?q=' and replace it with 'https://www.google.com/imgres?imgurl='
# this will take you to another page. Grab the source html again and put it
# in the soup to read again.
# look for '<a target="_blank"...' and grab the url from after 'data-href='
# This bring you to the image. Download it
