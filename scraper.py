'''
Created on Oct 10, 2014

@author: eotles
'''
import collections
import urllib2

game = collections.namedtuple('game', ['team1', 'team2', 'nominalValues'])


def main():
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    
    url = "http://www.sports-reference.com/cfb/years/2014-schedule.html"
    req = urllib2.Request(url, headers=hdr)
    try:
            page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    
    content = page.read()
    #print(content)
    
    printThis = False
    for line in content.splitlines():
        if(line.strip()  == '</tr>'):
            printThis = False
        if(printThis):
            print(line)
        if(line.strip()  == '<tr  class="ranked">'):
            printThis = True
    
    #soup = BeautifulSoup(open(url))
    #print(soup.prettify())
    
    

if __name__ == '__main__':
    main()