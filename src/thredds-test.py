import concurrent.futures
import urllib.request
import os

from remote import threddsBuilder
from remote import dateCarrier

def downloadList(path, urls):
    if not os.path.exists(path):
        os.makedirs(path)
    for url in urls:
        print(url)
        fname = url.split("/")
        fname = fname[len(fname) - 1]
        totalpath = path + fname
        urllib.request.urlretrieve(url, totalpath)
        print("Downloaded: {}".format(totalpath))
    print("Thread exit. Total: {} ".format(len(urls)))


# downloads every dataset that was uploaded for the date range (up until now)
# day = custom date via carrier class
def downloadCompleteDataset(day=None):
    datPath = "../data/thredds/"
    if not day.getQueryURI():
        day = threddsBuilder.getThreddsDayURI()

    dataset = threddsBuilder.getThreddsCompleteDataset(day.getQueryURI())

    for d in dataset:
        urls = threddsBuilder.getThreddsDownloadURLs(d.getQueryURI())
        datPath = "../data/thredds/{}/{}/".format("himawari9", d.getCompleteDateString())
        
        if len(urls) == 160:
            # lets split all the files into 4 chunks for a 4 threadded download and extract
            divCount = int(len(urls) / 4)
                
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                th1 = pool.submit(downloadList, datPath, urls[:divCount])
                th2 = pool.submit(downloadList, datPath, urls[divCount:divCount*2])
                th3 = pool.submit(downloadList, datPath, urls[divCount*2:divCount*3])
                th4 = pool.submit(downloadList, datPath, urls[divCount*3:divCount*4])
            
            pool.shutdown(wait=True)



downloadCompleteDataset(threddsBuilder.getThreddsDayCustomURI(dateCarrier.carrier("2024", "07", "04", "00", False)))