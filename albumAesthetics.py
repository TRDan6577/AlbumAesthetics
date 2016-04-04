"""
WARNING - SLOPPY CODE BELOW. WILL BE CLEANED
"""

from bs4 import BeautifulSoup
import mechanize
import re
import string

MULTIPLICATION = u"\xd7".encode('utf-8') # a multiplication symbol
TOLERANCE = 20  # max distance from a square image that we'll accept
IMAGE_SEARCH = 15  # Length of "/imgres?imgurl="
DELETION_SIZE = 7  # the size of the string "/url?q="
ACCEPTABLE_IMAGE_FORMATS = {".jpg", ".png", ".gif"}

print("[*] Creating the browser")
br = mechanize.Browser()
print("[*] Creating the http GET request")
br.set_handle_robots(False) # Be mean and ignore the site's request to not use robots
br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36')] # pretend we're a browser
html = br.open("https://www.google.com/search?q=acdc+back+in+black&safe=off&tbm=isch")
print("[+] Request sent!")

print("[*] Preparing the delicious soup")
# prepare some delicious soup
soup = BeautifulSoup(html.read(), 'html.parser')  # <-- Use a different parser for better speed?
print("[+] Soup ready!")

# We don't need the browser anymore
br.close()

# URLs for images searches on google:
# https://www.google.com/search?q=my+search+terms+here&safe=off&tbm=isch
# disected....                   |   1                | 2      | 3
# 1) Search result separated by spaces
# 2) Turn off safe search for all results
# 3) Set the type of search to an image search

# Then in print(soup.prettify()), look for the a href

print("[*] Getting the image URLs")
urls = []
for link in soup.find_all('a'):
    if(link.get('href') is not None and 
       string.find(str(link.get('href')), "/imgres?imgurl=") != -1):
        urls.append(link.get('href'))
print("[*] Retrieved image URLs")

# To find the size of the image, look for the multiplication sign
# (unicode) U+00D7 or \xd7

# Get all the sizes
sizes = soup.find_all(attrs={"class": "rg_ilmn"})

# Keep track of the highest resolution and it's corresponding index
highestResolution = 0
bestIndex = -1

# While we see a multiplication sign in the string, that means we have
# an image size. The format of the size string is 
# " length x width - sourceDomain "
for i in range(0, 19):

    curIndex = 1  # There's a space before the length
    sizeString = sizes[i].getText()

    # Set the length
    strLength = ''
    while(sizeString[curIndex].isdigit()):
        strLength = strLength + sizeString[curIndex]
        curIndex+=1
        # TODO: raise error here if you go out of index

    length = int(strLength)
    curIndex = curIndex + 3  # This puts us at the start of the width

    # Set the width
    strWidth = ''
    while(sizeString[curIndex].isdigit()):
        strWidth = strWidth + sizeString[curIndex]
        curIndex+=1
        # TODO: raise error here if you go out of index
    
    width = int(strWidth)

    # Check to see if the image is squarish
    if(abs(length - width) <= TOLERANCE):
        if(length * width > highestResolution):
            highestResolution = length * width
            bestIndex = i

    print("URL = " + urls[i])
    print("Has an image size of " + strLength + " x " + strWidth)
    print('\n')

# TODO: Check to see if highest resolution is zero or best index is -1

for imageType in ACCEPTABLE_IMAGE_FORMATS:
    if(imageType in urls[bestIndex]):
        imagePage = (urls[bestIndex])[IMAGE_SEARCH:(string.find(urls[bestIndex]
                     , imageType) + len(imageType))]

print(imagePage)

# Download the image
print("[*] Creating the browser")
br = mechanize.Browser()
print("[*] Creating the http GET request")
br.set_handle_robots(False) # Be mean and ignore the site's request to not use robots
br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36')] # pretend we're a browser
data = br.open(imagePage).read()
save = open("acdc back in black", 'wb')
save.write(data)
save.close()
br.close()
