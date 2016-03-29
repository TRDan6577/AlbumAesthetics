from bs4 import BeautifulSoup
import mechanize

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
