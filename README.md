# AlbumAesthetics
For those haunted in their sleep by pixelated nightmares

## Soooo what's the point?
For those of us that purchase/aquire music from places other than
[Amazon](http://www.amazon.com/MP3-Music-Download/b/ref=nav_shopall_dmusic?ie=UTF8&node=163856011),
[Google Music](https://music.google.com), and [iTunes](http://www.apple.com/itunes/),
we are burdened with either low quality or no album art at all leaving us sad. Given a string
to search for on [Google Images](https://images.google.com), this program finds the highest
resolution square(ish) photo and downloads it for you (within a default of 20 pixels of square 
so a 1500 x 1480 image would be downloaded)

## Installation
* Prerequisites - You MUST have python 2.7+ installed. You'll need to have the
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) python package installed. On Unix/Linux
systems, this can be installed with pip

`pip install BeautifulSoup`

Install Album Aesthetics with the git clone command

`git clone https://www.github.com/trdan6577/albumaesthetics.git`

## Yes, you too can bask in the HD glory (usage)
Currently, the only way to run it is from the command line:

`python albumAesthetics.py "artist name and their album in quotes"`

This is the most basic way to run the program. This results in the image and a .txt file
being placed in the same directory as the program. The .txt file contains the link where the
image came from.

##### Don't care where the image came from?
Use the '-n' or '--no-source-file' option to download just the image

##### Wait a sec, +-20 pixels means the image might not be exactly square!!!
Yep, great mathematical induction friend! If you want a perfectly square image, use the
'-t TOLERANCE' or '--tolerance TOLERANCE' option where TOLERANCE is the number of
pixels from square you'll allow

##### I just want to upload these images to another site
Some sites allow you to upload a photo by giving them a link. If you want the link to the
image, use the '-u' or '--url-only' options. Note that using this option does NOT create
the .txt file in your local directory

##### Entering in one search at a time is so tedious!
Search more than 1 album/artist combination by seperating them with colons in the quotes.
Example:

`python albumAesthetics.py "a day to remember for those who have heart:twenty one pilots blurryface:
ac dc back in black"`

## Future Plans
* File system scanning - automatically build searches based on nested folders
* Threading - Multiple album arts downloading at same time
