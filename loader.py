from time import sleep
import cfscrape
import urllib, urllib2
import bs4
import sys, os, getopt
import re
import beautifier as bf

class cookiestuff:
    def __init__(self):
        print "Connecting...\n"
        self.cookie_arg, self.user_agent = cfscrape.get_cookie_string("https://torrentproject.se")

ck = cookiestuff()

def getURL(st):
    return "https://torrentproject.se/?" + urllib.urlencode({'t': st})

def getIns():
    s = raw_input('Enter the search string: ')

    try:
        f = int(raw_input('Enter 1 if you want to download the first link as per the search. Else 0: '))
        if f not in [0,1]:
            raise ValueError
    except ValueError:
        print 'Please enter either a 0, or a 1'
        s, f = getIns()

    return s, f

def createReq(url):

    hdr = {
      'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'accept-encoding':'none',
      'accept-language':'en-GB,en-US;q=0.8,en;q=0.6',
      'cookie':ck.cookie_arg,
      'user-agent':ck.user_agent}

    req = urllib2.Request(url, headers = hdr)
    return req

def download(link, url, d):
    url = url.split('?')[0]
    url += link.get('href')[1:]
#print url
    req = createReq(url)
    x = urllib2.urlopen(req)

    try: os.mkdir('Torrents')
    except OSError: os.chdir('Torrents')

    soup = bs4.BeautifulSoup(x.read(), 'html.parser')
    tags = soup('span')

    for tag in tags:
        if u'class' in tag.attrs.keys():
            if u'download_torrent' in tag[u'class']:
                break

    lastu = tag.parent.contents[3].get('href')
    lastu = 'https:' + lastu
    req = createReq(lastu)
    x = urllib2.urlopen(req)

    nameproper = d['Name'].split()
    nameproper = nameproper[0] + nameproper[1] + u'.torrent'

    fp = open(nameproper, 'wb')

    print "\nCreating Torrent File...\n"
    sleep(1)
    fp.write(x.read())

    fp.close()

    print "Launching Torrent Client...\n"
    sleep(1)
    os.system('gnome-open ' + nameproper)
    print "Done\n"

def printDetails(lnk):
    print '==============DETAILS================\n\n'
    link = lnk.text
    d = dict()
    if link.find('(') > 0:
        d['Name'] = re.findall('^(.*) \(',link)[0].strip()
        if link.find(')'):
            d['Year'] = re.findall('\(([0-9]+)\)', link)[0].strip()
    else:
        d['Name'] = link
    x = re.findall(' [sS]([01][0-9])[eE]([012][0-9]) ', link)
    if x:
        d['Season'] = x[0][0].strip()
        d['Episode'] = x[0][1].strip()
    par = lnk.parent.parent.contents[1:]
    d['Seeders'] = par[0].text.strip()
    d['Leachers'] = par[1].text.strip()
    d['Time since upload'] = par[2].text.strip()
    d['Size'] = par[3].text.strip()
    bf.printer(d)
    print '\n\n====================================='

    return d

def htmlOperate(req, url, f=0, tr = 0):
    x = urllib2.urlopen(req)
    soup = bs4.BeautifulSoup(x.read(), 'html.parser')

    results = soup.find_all('a')[10:-14]
    count = 0

    if(f):
        link = results[tr]
    else:
        print
        for i in results:
            count += 1
            print str(count) + ' ' + i.text
        print
        print 'Select a Torrent:\nEnter 0 to Quit\n'
        try:
            choice = int(raw_input())
            if choice < 0 or choice > count: raise ValueError
        except ValueError:
            choice = int(raw_input('Please enter an INTEGER option IN the list: '))
            if type(choice) == type(str()) or choice < 0 or choice > count:
                sys.exit(2)
        if choice == 0: sys.exit(0)
        link = results[choice-1]


    d = printDetails(link)

    choice = 'z'
    while choice not in ['y', 'Y', 'n', 'N', 'Q', 'q'] :
        choice = raw_input('Do you want to download the torrent? (y/n): ')
        if choice in ['y', 'Y']:
            download(link, url, d)
        elif choice in ['n', 'N']:
            choice = raw_input('Enter q to Quit or n to try another one: ')
            if choice in ['q', 'Q']:
                sys.exit(0)

            os.system('clear')
            print('Refreshing')
            htmlOperate(req, url, f, tr + 1)
            return
        else:
            print 'Huh?'


def runner(par, opts = None):
    search_string = ''
    first_link = 0
    if par:
        if not(opts):
            print 'Note:\nCorrect usage is: python loader.py -s <search_string> -f <1_or_0>'
            sys.exit(2)
        for opt, arg in opts:
            if opt in ['-s', '--search']:
                search_string = arg
            elif opt in ['-f', '--firstlink']:
                if int(arg) in [0, 1]:
                    first_link = int(arg)
                else:
                    print 'Note:\nCorrect usage is: python loader.py -s <search_string> -f <1_or_0>'
                    sys.exit(2)
    else:
        search_string, first_link = getIns()

    url = getURL(search_string)
    req = createReq(url)
    htmlOperate(req, url, first_link)

def main(argv):
    if argv:
        try:
            opts, args = getopt.getopt(argv, 's:f:', 'search=firstlink=')
        except getopt.GetoptError:
            print 'Note:\nCorrect usage is: python loader.py [-s,--search] <search_string> [-f,--firstlink] <1_or_0>'
            sys.exit(2)
        runner(1, opts)
    else:
        runner(0)





if __name__ == '__main__':
    main(sys.argv[1:])
