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
import argparse
from bs4 import BeautifulSoup
import scanner
import string
import sys
import threading
import time
import urllib2

# Magic numbers and variables
IMAGE_SEARCH = 15  # The length of "/imgres?imgurl="
DELETION_SIZE = 7  # The length of "/url?q="
IMAGE_SEARCH_URL_PART1 = "https://www.google.com/search?q="
IMAGE_SEARCH_URL_PART2 = "&safe=off&tbm=isch"
ACCEPTABLE_IMAGE_FORMATS = {".jpg", ".png", ".gif", ".jpeg"}
THREAD_LOCK = threading.Lock()


class myThread(threading.Thread):
    """
    purpose: Holds the information necessary to download a picture
    """
    def __init__(self, searchTerm, TOLERANCE, writeFile, urlOnly, secondBest,
                 file, useScanner, artist=None, album=None, cwd=None):
        threading.Thread.__init__(self)
        self.TOLERANCE = TOLERANCE
        self.urlOnly = urlOnly
        self.writeFile = writeFile
        self.file = file
        self.useScanner = useScanner
        self.artist = artist
        self.album = album
        self.cwd = cwd
        self.secondBest = secondBest
        if(artist is not None and artist == album):
            self.searchTerm = artist + " self titled"
        else:
            self.searchTerm = searchTerm


    def run(self):
        getImage(self.searchTerm, self.TOLERANCE, not self.urlOnly, 
                self.writeFile, self.secondBest, self.file, self.useScanner,
                self.artist, self.album, self.cwd)


# Functions
def setArgParserOptions():
    """
    purpose: parses the command line arguments and returns it's findings
    :return: (NameSpace) the result of the command line arguments
    """
    parser = argparse.ArgumentParser(description='Get high-res album art',
                                     prog='albumAesthetics.py')
    parser.add_argument('searchTerm', metavar=('"Name of album and artist' +
                        ' in quotes"'), type=str, help=('Place the name of ' +
                        'the artist and album title in quotes. To enter' +
                        ' more than 1 artist and album, seperate each ' +
                        'artist/album combination with ":" (no double ' +
                        'quotes). To scan the current working directory' +
                        'for artist and album folders, do "scanner". To ' +
                        'specify a different directory to scan, do ' +
                        '"scanner:path/to/directory"'))

    # Add the option to not include a .txt file with the source
    parser.add_argument('-n', '--no-source-file', help=('Image sources are ' +
                        'not cited in a .txt file'), action='store_true',
                        dest='writeFile')
    # Add the option to change the tolerance from square
    parser.add_argument('-t', '--tolerance', help=('Sets the tolerance from' +
                        ' square (ex: 393x400 would be within 7 tolerance)'),
                        type=int)

    # Add the option to print the url of the image rather than downloading it
    parser.add_argument('-u', '--url-only', help=('Don\'t download the image.' +
                        ' Instead, print the image url to stdout'),
                        action='store_true', dest='urlOnly')

    parser.add_argument('-s', '--second-best', help=('Gives you the second ' +
                        'highest resolution image. See the README.md for ' +
                        'info on why you\'d want this command'),
                        action='store_true', dest='secondBest')

    return parser.parse_args()


def findHighestRes(sizes, TOLERANCE, secondBest):
    """
    purpose: finds the highest square resolution in the first twenty search
             results
    :param sizes: (list) a list of Tag objects that contain the image size.
                  For info on Tag objects, see the BeautifulSoup docs
    :param TOLERANCE: (int) Max distance from a square image that we'll accept
    :param secondBest: (bool) Tells us to return the second highest resolution
                  image instead of the highest resolution
    :return: (int) index of the desired image
    """
    # Keep track of the highest resolution and it's corresponding index
    highestResolution = 0
    bestIndex = -1
    if(secondBest):
        secondBestIndex = -1
        secondResolution = 0

    # Look through the sizes and find the highest (squarish) resolution image
    for i in range(0, 19):

        curIndex = 1  # There's a space before the length
        sizeString = sizes[i].getText()
        sizeStringLength = len(sizeString)

        # Set the length
        strLength = ''
        while(sizeString[curIndex].isdigit()):
            strLength = strLength + sizeString[curIndex]
            curIndex += 1
            if(curIndex >= sizeStringLength):
                print("An error occured while parsing an image's size")
                sys.exit(0)

        curIndex = curIndex + 3  # This puts us at the start of the width

        # Set the width
        strWidth = ''
        while(sizeString[curIndex].isdigit()):
            strWidth = strWidth + sizeString[curIndex]
            curIndex += 1
            if(curIndex >= sizeStringLength):
                print("An error occured while parsing an image's size")
                sys.exit(0)

        length = int(strLength)
        width = int(strWidth)

        # Check to see if the image is squarish
        if(abs(length - width) <= TOLERANCE):
            # If so, see if it's the highest resolution we've seen so far
            if(length * width > highestResolution):
                highestResolution = length * width
                bestIndex = i

            # Determine if it's the second highest resolution we've seen
            if(secondBest and (length*width > secondResolution) and 
               length*width < highestResolution):
                secondResolution = length * width
                secondBestIndex = i

    if(secondBest):
        return secondBestIndex
    else:
        return bestIndex


def getHTML(URL):
    """
    purpose: crafts the http GET message to send to URL and gives the user the
             resulting html code
    :param URL: (str) The URL to open
    :return: (Not sure which type because the urllib2 docs don't really
             specify) the opened html page
    """

    # Create the broswer
    request = urllib2.Request(URL)

    # Create the HTTP GET headers
    request.add_header('User-Agent', ('Mozilla/5.0 (Windows NT 6.1; WOW64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      ' Chrome/43.0.2357.125 Safari/537.36'))

    # Return the result of the sent request
    return urllib2.urlopen(request)


def main():
    """
    purpose: the main running function to get the hd album art
    """
    # Parse the args with argparse
    args = setArgParserOptions()

    # Set the options based on the arguments
    
    # Assume they don't want to use the scanner for now
    useScanner = False
    cwd = None

    # Set the tolerance (default is 20)
    if(args.tolerance is not None):
        TOLERANCE = args.tolerance
    else:
        TOLERANCE = 20  # The max dist from a square image that we'll accept

    # Determine whether or not to write the source text file
    if(args.urlOnly):
        writeFile = False
    else:
        writeFile = not args.writeFile

    # ARe we getting the second best image?
    if(args.secondBest):
        secondBest = True
    else:
        secondBest = False

    # Set the search terms
    searchTerms = args.searchTerm.split(':')

    # See if they want to use the scanning ultility
    if(len(searchTerms) <= 2 and searchTerms[0] == 'scanner'):
        useScanner = True
        
        # See if they specifed a directory
        if(len(searchTerms) == 2):
            cwd = searchTerms[1]

    # Open the sources file only if we are going to write to it
    if(writeFile):
        file = open('sources.txt', 'wb')
    else:
        file = None

    threads = []

    # If they didn't specify to use the scanner, use the searchTerms
    if(not useScanner):
        for i in range(0, len(searchTerms)):
            threads.append(myThread(searchTerms[i], TOLERANCE, writeFile, 
                          args.urlOnly, secondBest, file, useScanner))
            threads[i].start()
    # Otherwise, use the scanner
    else:
        i = 0

        # Create a thread for each album/artist combination
        if(cwd):
            for artist, album in scanner.getAlbums(ACCEPTABLE_IMAGE_FORMATS, cwd):
                threads.append(myThread(artist + " " + album, TOLERANCE,
                               writeFile, args.urlOnly, secondBest, file,
                               useScanner, artist, album, cwd))
                threads[i].start()
                i += 1
        else:
            for artist, album in scanner.getAlbums(ACCEPTABLE_IMAGE_FORMATS):
                threads.append(myThread(artist + " " + album, TOLERANCE,
                               writeFile, args.urlOnly, secondBest, file, 
                               useScanner, artist, album))
                threads[i].start()
                i += 1

    # Wait for all the threads to finish finding their image
    for thread in threads:
        thread.join()

    # Close the file if needed
    if(not args.urlOnly and writeFile):
        file.close()


def getImage(searchTerm, TOLERANCE, saveImage, writeFile, secondBest, file,
             useScanner, artist=None, album=None, cwd=None):
    # Get the webpage
    html = getHTML(IMAGE_SEARCH_URL_PART1 + searchTerm.replace(" ", "+") +
                   IMAGE_SEARCH_URL_PART2)

    if(html is None):
        print("An error occurred while opening the webpage")
        file.close()
        return 0

    # prepare some delicious soup (parse the html with BeautifulSoup)
    soup = BeautifulSoup(html.read(), 'html.parser')

    # Find the urls in the metadata
    urls = []
    bestImageType = None  # The filetype of the image to append to the filename
    for data in soup.find_all(attrs={'class': 'rg_meta'}):
        # For each metadata entry, if it contains more than 10 entries,
        # then parse it for the URL
        if(len(data.getText().split(',')) > 10):
            for element in data.getText().split(','):
                time.sleep(.001)
                # Look for '"ou":"http' and a .gif, .png, or .jpg
                if(string.find(element, '"ou":"http') != -1):
                    for imageType in ACCEPTABLE_IMAGE_FORMATS:
                        if(string.find(element, imageType) != -1):
                            # If found, append just the URL
                            urls.append(element[6:-1])
                            bestImageType = imageType

    # Get all the sizes
    sizes = soup.find_all(attrs={"class": "rg_ilmn"})

    # Get the index of the highest quality album art
    bestIndex = findHighestRes(sizes, TOLERANCE, secondBest)

    # If the index is -1, no acceptable image was found. Exit
    if(bestIndex == -1):
        print("No album artwork found within the acceptable tolerance")
        print("You can change the tolerance with -t (use -h for more help)")
        file.close()
        return 0

    # Get the HTML for the image
    html = getHTML(urls[bestIndex])
    if(html is None):
        print("An error occurred while opening the webpage")
        file.close()
        return 0

    # If we don't just want to print the URL to stdout
    if(saveImage):
        # Save the image
        
        # If they used the scanner, put the image in the approriate folder
        if(useScanner):
            if(cwd is None):
                scanner.writeImage(html.read(), artist, album, bestImageType)
            else:
                scanner.writeImage(html.read(), artist, album, bestImageType,
                                   cwd)
        # Otherwise, put the image in the current working directory
        else:
            img = open(searchTerm, 'wb')
            img.write(html.read())
            img.close()

        # Give credit to the source by writing the image url to a txt file
        if(writeFile):
            # Make sure we're the only ones writing to the file
            THREAD_LOCK.acquire()
            file.write(urls[bestIndex] + '\n')
            THREAD_LOCK.release()
    else:
        print(urls[bestIndex])

if __name__ == "__main__":
    main()
