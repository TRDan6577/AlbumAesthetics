import os

def getAlbums(cwd=os.getcwd()):
    """
    purpose: parses the cwd for directory names and sub directory names.
             With those names, it builds and returns an artist and an
             album for each of the sub directories
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
            if(os.path.isdir(os.path.join(cwd, os.path.join(artist, file)))):
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
