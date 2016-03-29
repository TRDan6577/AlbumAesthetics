# AlbumAesthetics
For those haunted in their sleep by pixelated nightmares

## Soooo what's the point?
For those of us that purchase/aquire music from places other than
[Amazon](http://www.amazon.com/MP3-Music-Download/b/ref=nav_shopall_dmusic?ie=UTF8&node=163856011),
[Google Music](https://music.google.com), and [iTunes](http://www.apple.com/itunes/),
we are burdened with either low quality or no album art at all leaving us sad. Given a string
to search for on [Google Images](https://images.google.com), this program finds the highest
resolution square(ish) photo and downloads it for you (within 20 pixels of sqare so a 1500 x 1480
image would be downloaded)

## Installation
* Prerequisites - You'll need to have the following python packages installed:
[mechanize](http://wwwsearch.sourceforge.net/mechanize/) and
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/). On Unix/Linux systems, these can be
installed with pip

> `pip install mechanize`

> `pip install BeautifulSoup`

Install Album Aesthetics with the git clone command

> `git clone https://www.github.com/trdan6577/albumaesthetics.git`

## Disclaimer:
This is not finished and is currently a work in progress

### Future Plans
* Multiple search strings (separated by colons? "hey hey : yo yo")
* File system scanning - automatically build searches based on nested folders
* Sleep between multiple searches so google doesn't block you
* Add an option to not sleep between searches
* Add an option to NOT download photo but to give user the url instead
* Add an option to change the allowed distance from square to +- 20 pixels