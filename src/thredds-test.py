import concurrent.futures
import urllib.request

import threddsclient

from remote import dateUtil

datPath = "../data/thredds/"


def genThreddsUrl():
     dd = dateUtil.getLatestDateCarrier(negativeOffset=0)
     url = "https://thredds.nci.org.au/thredds/catalog/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/{}/catalog.xml".format(dd.getStdQueryString())
     dd.setQueryURI(url)
     print(url)
     return dd
     

def downloadWrapper(path, urls):
    for url in urls:
        fname = url.split("/")
        fname = fname[len(fname) - 1]
        totalpath = path + fname
        urllib.request.urlretrieve(url, totalpath)
        print("Downloaded: {}".format(totalpath))
    print("Thread exit. Total: {} ".format(len(urls)))


obj = genThreddsUrl()
test = threddsclient.download_urls(obj.getQueryURI())
print(len(test))

if False:
     
    if (int(len(urls)) % 2) == 0: 
            
            # lets split all the files into 4 chunks for a 4 threadded download and extract
            divCount = int(len(urls) / 4)
            
            with sconcurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                th1 = pool.submit(downloadWrapper, datPath, urls[:divCount])
                th2 = pool.submit(downloadWrapper, datPath, urls[divCount:divCount*2])
                th3 = pool.submit(downloadWrapper, datPath, urls[divCount*2:divCount*3])
                th4 = pool.submit(downloadWrapper, datPath, urls[divCount*3:divCount*4])
        
            pool.shutdown(wait=True)


            
