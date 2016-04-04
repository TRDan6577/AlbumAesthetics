"""
File: albumAesthetics.py
Author: Tom Daniels <trd6577@g.rit.edu>
Purpose: Gets high resolution album art for your music library
"""

# A little background at what's going on
"""
URLs for images searches on google:
https://www.google.com/search?q=my+search+terms+here&safe=off&tbm=isch
disected....                   |   1                | 2      | 3
1) Search result separated by spaces
2) Turn off safe search for all results
3) Set the type of search to an image search
"""

# Imports
from bs4 import BeautifulSoup
import mechanize
import re
import string
import sys

# Magic numbers and variables
TOLERANCE = 20  # The max distance from a square image that we'll accept
IMAGE_SEARCH = 15  # The length of "/imgres?imgurl="
DELETION_SIZE = 7  # The length of "/url?q="
IMAGE_SEARCH_URL_PART1 = "https://www.google.com/search?q="
IMAGE_SEARCH_URL_PART2 = "&safe=off&tbm=isch"  # Turn off safe search and turn
                                               # on image search
ACCEPTABLE_IMAGE_FORMATS = {".jpg", ".png", ".gif"}

# Functions
def findHighestRes(sizes):
    """
    purpose: finds the highest square resolution in the first twenty search
             results
    :param sizes: (list) a list of Tag objects that contain the image size.
                  For info on Tag objects, see the BeautifulSoup docs
    :return: (int) index of the highest resolution
    """
    # Keep track of the highest resolution and it's corresponding index
    highestResolution = 0
    bestIndex = -1

    # Look through the sizes and find the highest (squarish) resolution image
    for i in range(0, 19):

        curIndex = 1  # There's a space before the length
        sizeString = sizes[i].getText()

        # Set the length
        strLength = ''
        while(sizeString[curIndex].isdigit()):
            strLength = strLength + sizeString[curIndex]
            curIndex+=1
            # TODO: raise error here if you go out of index

        curIndex = curIndex + 3  # This puts us at the start of the width

        # Set the width
        strWidth = ''
        while(sizeString[curIndex].isdigit()):
            strWidth = strWidth + sizeString[curIndex]
            curIndex+=1
            # TODO: raise error here if you go out of index
        
        length = int(strLength)
        width = int(strWidth)

        # Check to see if the image is squarish
        if(abs(length - width) <= TOLERANCE):
            # If so, see if it's the highest resolution we've seen so far
            if(length * width > highestResolution):
                highestResolution = length * width
                bestIndex = i

    return bestIndex


def getHTML(URL):
    """
    purpose: crafts the http GET message to send to URL and gives the user the
             resulting html code
    :param URL: (str) The URL to open
    :return: (Not sure which type because the python mechanize documentation 
             is bad) the opened html page
    """

    # Create the broswer
    br = mechanize.Browser()

    # Create the HTTP GET headers
    br.set_handle_robots(False) # Be mean and ignore the site's request to not use robots
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36')] # pretend we're a browser
    
    # Return the result of the sent request
    return br.open(URL)
    # TODO: Make sure the value returned is not None


def main():
    # TODO: Check the command line args. Make sure artist/album in quotes
    searchTerm = str(sys.argv[1])

    # Get the webpage
    html = getHTML(IMAGE_SEARCH_URL_PART1 + searchTerm.replace(" ", "+") +
           IMAGE_SEARCH_URL_PART2)

    # prepare some delicious soup (parse the html with BeautifulSoup)
    soup = BeautifulSoup(html.read(), 'html.parser')  # <-- Use a different parser for better speed?

    # Get all the hrefs that contain an image url
    urls = []
    for link in soup.find_all('a'):
        if(link.get('href') is not None and 
           string.find(str(link.get('href')), "/imgres?imgurl=") != -1):
            urls.append(link.get('href'))

    # Get all the sizes
    sizes = soup.find_all(attrs={"class": "rg_ilmn"})
    
    bestIndex = findHighestRes(sizes)
    # TODO: Check to see if best index is -1

    # Find the substring that actually contains the image url
    for imageType in ACCEPTABLE_IMAGE_FORMATS:
        if(imageType in urls[bestIndex]):
            imagePage = (urls[bestIndex])[IMAGE_SEARCH:(string.find(urls[bestIndex]
                         , imageType) + len(imageType))]

    # Download the image
    html = getHTML(imagePage)
    data = html.read()
    save = open(searchTerm, 'wb')
    save.write(data)
    save.close()


if __name__ == "__main__":
    main()
