from googleapiclient.discovery import build
import sys
import socks
import socket
from bs4 import BeautifulSoup
import requests
import utils
import csv
import pymongo
from mongo import insert, save_additional_details, save_pros_and_cons
from difflib import SequenceMatcher

reload(sys)
sys.setdefaultencoding("utf8")

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
        addr='127.0.0.1', port=9050)

socket.socket = socks.socksocket

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
}
service = build("customsearch",'v1', developerKey="AIzaSyBvSxGvp8S7YAAMzp3CKaBc40TMWVNAweg")

def getPhoneDetails(search):
    
    res = service.cse().list(q=search, cx="016617856427036748002:mblvnhdtjp4").execute()
    if int(res["searchInformation"]["totalResults"]) > 0:
        u = res["items"][0]["link"]
        print u
        getByUrl(u)
 

def getByUrl(u):
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
    if data != {}:
        bool = insert(data)
        if bool:
            try:
                if data["Model"] is None:
                    print 'No Name Found'
                else:
                    getProsandCons(data["Model"])
            except:
                print 'No Name Found'
    return data






def getProsandCons(model_name):
    
    print model_name
    res = service.cse().list(q=model_name + " specs", cx="016617856427036748002:eamia_g5foe").execute()
  
    if int(res["searchInformation"]["totalResults"]) > 0:
        u = res["items"][0]["link"]
        print u
        r = requests.get(u, headers=utils.merge(DEFAULT_HEADERS, {}))
        soup = BeautifulSoup(r.text, 'lxml')
        data = {}
        data["name"] = model_name
        data["pros"] = []
        data["cons"] = []
        for li in soup.select('.pros > li'):
            data["pros"].append(li.contents[0])
    
    
        for li in soup.select('ul.cons > li'):
            data["cons"].append(li.contents[0])
        print data
        save_pros_and_cons(data)

    getComparisons(model_name)



def getComparisons(model_name):
   
    res = service.cse().list(q=model_name + "", cx="016617856427036748002:sdc91k8hcbi").execute()
    if int(res["searchInformation"]["totalResults"]) > 0:
        for item in res["items"]:
            u = item["link"]
    
            r = requests.get(u, headers=utils.merge(DEFAULT_HEADERS, {}))
            soup = BeautifulSoup(r.text, 'lxml')
            data = {}
            count = 0

            for tr in soup.select('table.diffs > tr'):
                if  len(tr.select('th > h2 > em > span.tr-prod')) > 0:
                    count += 1
                    name =  tr.select('th > h2 > em > span.tr-prod')[0].contents[0]

                    data["data"+str(count)] = {}
                    data["data"+str(count)]["name"] = name
                    data["data"+str(count)]["ratio"] = SequenceMatcher(None, model_name, name).ratio()
                    data["data"+str(count)]["betterThanFeatures"] = []

                    print name
                elif count == 0:
                    continue
                else:
                    if len(tr.select('td')) > 6:
                        data["data"+str(count)]["betterThanFeatures"].append(tr.select('td')[2].contents[0])
                        # can use other info here as well


            # process the data and save
            findPrimary(data["data1"],data["data2"],model_name)
            print data
        


def findPrimary(data1,data2, model_name):
    if data1["ratio"] > data2["ratio"]:
        primary = data1
        secondary = data2

    else:
        secondary = data1
        primary = data2

    primary["name"] = model_name
 
    primary["compareModel"] = secondary["name"]
    secondary["compareModel"] = primary["name"]

    primary["worseThanFeatures"] = secondary["betterThanFeatures"]
    secondary["worseThanFeatures"] = primary["betterThanFeatures"]

    getSecondaryName(primary,secondary)


def getSecondaryName(primary,secondary):
    res = service.cse().list(q=secondary["name"], cx="006500068614198421475:-wsj6q61h0e").execute()
    if int(res["searchInformation"]["totalResults"]) > 0:
        u = res["items"][0]["link"]
        print u
    
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



        if data != {}:
            try:
                if data["Model"] is None:
                    print 'No Name Found'
                else:
                    print "secondary found:"
                    print data["Model"] 
                    secondary["name"] = data["Model"]
                    bool = insert(data)
                    if bool:
                        print "saved: "
                        print "getting details for: "
                        print secondary["name"]
                        getProsandCons(secondary["name"])
            except:
                print 'No Name Found'


    save_additional_details(primary,secondary)


# getProsandCons("Samsung Galaxy S7 specs")
# data = getPhoneDetails('htc A9')

# getPhoneDetails("Samasung Galaxy S8")
# getPhoneDetails("Sony Xperia Z")
# getPhoneDetails("Apple iPhone 8")
# getPhoneDetails("Apple iPhone 7")
# getPhoneDetails("HTC U11")
# getPhoneDetails("One plus 5")
# getPhoneDetails("Google Pixel")