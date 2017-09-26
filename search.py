from googleapiclient.discovery import build
import sys
import socks
import socket
from bs4 import BeautifulSoup
import requests
import utils
import csv
import pymongo
from mongo import insert

reload(sys)
sys.setdefaultencoding("utf8")

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
        addr='127.0.0.1', port=9050)

socket.socket = socks.socksocket

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
}

def getPhoneDetails(search):
    service = build("customsearch",'v1', developerKey="AIzaSyBvSxGvp8S7YAAMzp3CKaBc40TMWVNAweg")

    res = service.cse().list(q=search, cx="006500068614198421475:-wsj6q61h0e").execute()

    u = res["items"][0]["link"]
    print u


    print 'url', u
    r = requests.get(u, headers=utils.merge(DEFAULT_HEADERS, {}))
    soup = BeautifulSoup(r.text, 'lxml')
    data = {}
    # name = soup.select('.specs-phone-name-title')[0].contents[0]
    try:
        for t in soup.select('table'):
            h = []
            for e in t.select('.ttl > a'):
                h.append(e.contents[0])
            c=[]
            for e in t.select('.nfo'):
                if e.contents:
                    c.append(e.contents[0])
            section = t.select('th')[0].contents[0]
            data.update(dict(zip(h, c)))
        title = soup.select('.specs-phone-name-title')[0].get_text()
        data.update({'Model': title})
        if 'Technology' in data:
            data['Technology'] = str(data['Technology']).strip('<a class="link-network-detail collapse" href="#"></a>')
    except:
        print '404'

    print data
    return data

# data = getPhoneDetails('htc A9')
# if data != {}:
#     insert(data)
 