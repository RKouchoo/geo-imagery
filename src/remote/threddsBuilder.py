import urllib.request
import xml.etree.ElementTree as etree
import os

import dateUtil
import dateCarrier


# attempt to get the latest thredds URI  based on system time 
# pass an offset time if you think the server is slow
def genThreddsUrl():
    dd = dateUtil.getLatestDateCarrier(negativeOffset=0)
    url = "https://thredds.nci.org.au/thredds/catalog/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/{}/catalog.xml".format(dd.getStdQueryString())
    dd.setQueryURI(url)
    print(url)
    return dd


# generate the link to todays XML file 
def getThreddsDayURI():
    dd = dateUtil.getLatestDateCarrier(negativeOffset=0)
    url = "https://thredds.nci.org.au/thredds/catalog/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/{}/{}/{}/catalog.xml".format(dd.getYear(), dd.getMonth(), dd.getDay())
    dd.setQueryURI(url)
    return(dd)


# create a custom URI helper method
def genThreddsCustomURI(date=dateUtil.getLatestDateCarrier()):
    url = "https://thredds.nci.org.au/thredds/catalog/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/{}/{}/{}/{}/catalog.xml".format(date.getYear(), date.getMonth(), date.getDay(), date.getTime())
    date.setQueryURI(url)
    date.setIsGenerated(True)
    return date


# lets generate a list of carrier objects for ever nested XML 
def getThreddsCompleteDataset(todayXML):
    # download the xml first
    urllib.request.urlretrieve(todayXML, "today.xml")
    tree = etree.parse("today.xml").getroot()[3]
    cats = []
    for child in tree:
        id = child.attrib.get("ID")
        if id is not None:
            tms = id.split("/")
            cats.append(genThreddsCustomURI(date=dateCarrier.carrier(tms[1], tms[2], tms[3], tms[4], True)))       

    os.remove("today.xml")
    return cats
    

# https://thredds.nci.org.au/thredds/catalog/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/2024/07/04/0000/catalog.xml
# https://thredds.nci.org.au/thredds/fileServer/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/2024/07/04/0000/HS_H09_20240704_0000_B01_FLDK_R10_S0110.DAT
# https://thredds.nci.org.au/thredds/fileserver/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/2024/07/04/0000/HS_H09_20240704_0000_B01_FLDK_R10_S0110.DAT
#                                        ^ this typo cost me forever
# returns a list of downloadable URLs for a day
# supply path to the container URL
def getThreddsDownloadURLs(containerXML):
    urllib.request.urlretrieve(containerXML, "container.xml")
    tree = etree.parse("container.xml").getroot()
    base =  str(containerXML).split("catalog/")[0]

    dl = []
    for child in tree[3]:
        id = child.attrib.get("urlPath")
        if id is not None:
            dl.append("{}fileServer/{}".format(base, str(id)))

    os.remove("container.xml")
    return(dl)
            
