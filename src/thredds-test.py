import concurrent.futures
import urllib.request

import threddsclient

urls = threddsclient.download_urls("https://thredds.nci.org.au/thredds/catalog/gc63/satellite-products/nrt/raw/himawari-ahi/fldk/latest/2024/07/03/0710/catalog.xml")

datPath = "../data/thredds/"


def downloadWrapper(path, urls):
    for url in urls:
        fname = url.split("/")
        fname = fname[len(fname) - 1]
        totalpath = path + fname
        urllib.request.urlretrieve(url, totalpath)
        print("Downloaded: {}".format(totalpath))
    print("Thread exit. Total: {} ".format(len(urls)))


if (int(len(urls)) % 2) == 0: 
        
        # lets split all the files into 4 chunks for a 4 threadded download and extract
        divCount = int(len(urls) / 4)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            th1 = pool.submit(downloadWrapper, datPath, urls[:divCount])
            th2 = pool.submit(downloadWrapper, datPath, urls[divCount:divCount*2])
            th3 = pool.submit(downloadWrapper, datPath, urls[divCount*2:divCount*3])
            th4 = pool.submit(downloadWrapper, datPath, urls[divCount*3:divCount*4])
    
        pool.shutdown(wait=True)


            
