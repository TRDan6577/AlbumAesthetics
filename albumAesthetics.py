"""
WARNING - SLOPPY CODE BELOW. WILL BE CLEANED
"""

from bs4 import BeautifulSoup
import mechanize
import re
import string

MULTIPLICATION = u"\xd7".encode('utf-8') # a multiplication symbol
TOLERANCE = 20 # max distance from a square image that we'll accept
IMAGE_SEARCH = "https://www.google.com/imgres?imgurl="
DELETION_SIZE = 7 # the size of the string "/url?q="

br = mechanize.Browser()
br.set_handle_robots(False) # Be mean and ignore the site's request to not use robots
br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36')] # pretend we're a browser
html = br.open("https://www.google.com/search?q=this+is+a+test&safe=off&tbm=isch")

# prepare some delicious soup
soup = BeautifulSoup(html.read(), 'html.parser')

# URLs for images searches on google:
# https://www.google.com/search?q=my+search+terms+here&safe=off&tbm=isch
# disected....                   |   1                | 2      | 3
# 1) Search result separated by spaces
# 2) Turn off safe search for all results
# 3) Set the type of search to an image search

# Then in print(soup.prettify()), look for the a href.

"""
come up with a faster way. If you get the urls this way,
you still need to parse them once more. If you get the URLs
and their corresponding picture sizes at the same time, you
only need to go through all of the urls once
"""

urls = []

for link in soup.find_all('a'):
    if(string.find(link.get('href'), "/images?imgurl=") != -1):
        urls.append(link.get('href'))

# To find the size of the image, look for the multiplication sign
# (unicode) U+00D7 or \xd7


# sizeFinder iterates over the 'br' tags looking for the size of the image
sizeFinder = soup.a
sizeFinder = sizeFinder.find_next('br') # Find the first <br></br> tag
sizeFinder = sizeFinder.find_next('br')
sizeFinder = sizeFinder.find_next('br')
brString = sizeFinder.getText().encode('utf-8')
urlIndex = 0 # Keep track of which URL we're looking at

# Keep track of the highest resolution and it's corresponding index
highestResolution = 0
bestIndex = -1

# While we see a multiplication sign in the string, that means we have
# an image size
while(string.find(brString, MULTIPLICATION) != -1):

    curIndex = 0

    # Set the length
    strLength = ''
    while(brString[curIndex].isdigit()):
        strLength = strLength + brString[curIndex]
        curIndex+=1
        # TODO: raise error here if you go out of index

    length = int(strLength)
    curIndex = curIndex + 4 # This puts us at the start of the width

    # Set the width
    strWidth = ''
    while(brString[curIndex].isdigit()):
        strWidth = strWidth + brString[curIndex]
        curIndex+=1
        # TODO: raise error here if you go out of index
    
    width = int(strWidth)

    # Check to see if the image is squarish
    if(abs(length - width) <= TOLERANCE):
        if(length * width > highestResolution):
            highestResolution = length * width
            bestIndex = urlIndex

    print("URL = " + urls[urlIndex])
    print("Has an image size of " + strLength + " x " + strWidth)
    print('\n')

    sizeFinder = sizeFinder.find_next('br')
    if(sizeFinder is None):
        break
    sizeFinder = sizeFinder.find_next('br')
    if(sizeFinder is None):
        break
    sizeFinder = sizeFinder.find_next('br')
    if(sizeFinder is None):
        break
    brString = sizeFinder.getText().encode('utf-8')
    urlIndex+=1

# TODO: Check to see if highest resolution is zero or best index is -1

imagePage = IMAGE_SEARCH + (urls[bestIndex])[DELETION_SIZE:]

print(imagePage)

# Get rid of the 
# '/url?q=' and replace it with 'https://www.google.com/imgres?imgurl='
# this will take you to another page. Grab the source html again and put it
# in the soup to read again.
# look for '<a target="_blank"...' and grab the url from after 'data-href='
# This bring you to the image. Download it
