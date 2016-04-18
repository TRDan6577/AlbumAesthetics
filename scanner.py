"""
File: scanner.py
Purpose: Functions that interface with the user's directory
Author: Thomas Daniels <trd6577@g.rit.edu>
"""
import os


def getAlbums(ACCEPTABLE_IMAGE_FORMATS, cwd=os.getcwd()):
    """
    purpose: parses the cwd for directory names and sub directory names.
             With those names, it builds and returns an artist and an
             album for each of the sub directories
    :param ACCEPTABLE_IMAGE_FORMATS: (list) a list of strings contianing
             image format endings (.jpg, .png, etc)
    :param cwd: (path) the path to parse. If none given, set it to the cwd
    :return: (list: [str, str]) returns a list of artists and albums
    """

    searches = []  # A list of tuples (str, str) artist, album
    artists = []  # A list of artists

    # Create the list of artists (the sub directories in the cwd)
    for file in os.listdir(cwd):
        if(os.path.isdir(os.path.join(cwd, file))):
            artists.append(file)

    # Get the albums for each of the artists
    for artist in artists:
        for file in os.listdir(os.path.join(cwd, artist)):
            path = os.path.join(cwd, os.path.join(artist, file))
            # For each directory, if it doesn't contain the image file
            # then add it to the list of images to search for
            if(os.path.isdir(path)):
                addSearch = True
                for filename in os.listdir(path):
                    # Look to see if the directory already contians an image
                    for img in ACCEPTABLE_IMAGE_FORMATS:
                        if(os.path.isfile(os.path.join(path, filename)) and
                           img in filename):
                            addSearch = False
                    # If it doesn't contain an image, add it to the search
                    if(not os.path.isfile(os.path.join(path, filename)) and
                       addSearch):
                        searches.append((artist, file))

    return searches


def writeImage(img, artist, album, imgType, cwd=os.getcwd()):
    """
    purpose: writes the image to the correct folder
    :param img: (data) the image to be written to the file
    :param artist: (str) the artist
    :param album: (str) an album belonging to artist
    :param imgType: (str) the type of image (jpg, png, gif, etc)
    :param cwd: (str) the music directory
    :return: (Nonetype) none
    """

    imgFile = open(os.path.join(os.path.join(cwd, os.path.join(artist, album)),
                   (artist + " " + album + imgType)), 'wb')
    imgFile.write(img)
    imgFile.close()
