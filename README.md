torrent-finder
==============

An easy to use Python module/application that is capable of locating and downloading the most relevant and recent '.torrent' according to the supplied search-string.

It makes use of [cfscrape](https://github.com/Anorov/cloudflare-scrape), that allows for the application to *harmlessly* scrape the required torrent indexing websites.

The search-string can be directly supplied as a **command-line arguement** from the linux terminal.

Dependancies
============

- Python 2.7 or greater.
- [cfscrape](https://github.com/Anorov/cloudflare-scrape) **NOTE**: cfscrape in itself requires the following dependancies:
-- [Js2Py](https://github.com/PiotrDabkowski/Js2Py)
-- [Requests](https://github.com/kennethreitz/requests)
-- Cloning the **cfscrape module** and running the following command will automatically install all dependancies.

<pre>
<code>
    python setup.py install
</code>
</pre>
    
- The beautifier Module provided in this package: It is a pretty printer for Nested Dictionaries and lists
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup)**: A module that parser HTML and XML in Python.


Usage
=====

It can be invoked from the command line. 

<table>
  <tr>
  <td>Parameter</td>
  <td>Relevance</td>
  <td>Range</td>
  </tr>
  <tr>
  <td>Short: -s, Long: --search</td>
  <td>You use this to denote the search-string</td>
  <td>It can be any valid string. If greater than 1 word enclose in quotes</td>
  </tr>
  <tr>
  <td>Short: -f, Long: --firstlink</td>
  <td>Similar to the "I'm Feeling Lucky" on Google, it causes the program to automatically display the highest ranked torrent and skip the other ones.
  </td>
  <td>0 - Unset, 1 - Set</td>
  </tr>
</table>
   
##Examples

<pre>
Short Parameters:
    <code>
    python loader.py -s "Ubuntu LTS" -f 1
    </code>
Long Parameters:
    <code>
    python loader.py --search Ubuntu --firstlink 0 
    </code>
</pre>(

The downloaded '.torrent' file is **automatically launched** via the default application for '.torrent' files. 
Please select a default application beforehand for smoother execution in the following way:
- Right clicking a torrent file.
- Clicking on "Open With".
- Choosing your preferred BitTorrent Client.
- And finally selecting "Set as default".


####Note: The torrent files are received from a 3rd party. [Torrent Project](https://torrentproject.se) is being used by the crawler/scraper as the files are arranged according to relevance.
