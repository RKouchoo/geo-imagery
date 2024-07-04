import concurrent.futures
import urllib.request


from remote import threddsBuilder


def download(path, urls):
    for url in urls:
        fname = url.split("/")
        fname = fname[len(fname) - 1]
        totalpath = path + fname
        urllib.request.urlretrieve(url, totalpath)
        print("Downloaded: {}".format(totalpath))
    print("Thread exit. Total: {} ".format(len(urls)))



# downloads every dataset that was uploaded today (up until now)

def downloadToday():

    datPath = "../data/thredds/"
    day = threddsBuilder.getThreddsDayURI()
    dataset = threddsBuilder.getThreddsCompleteDataset(day.getQueryURI())

    for d in dataset:
        urls = threddsBuilder.getThreddsDownloadURLs(d.getQueryURI())
        datPath = "../data/thredds/{}/{}/".format("himawari9", d.getCompleteDateString())

        if (int(len(urls)) % 2) == 0: 
                
                # lets split all the files into 4 chunks for a 4 threadded download and extract
                divCount = int(len(urls) / 4)
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                    th1 = pool.submit(download, datPath, urls[:divCount])
                    th2 = pool.submit(download, datPath, urls[divCount:divCount*2])
                    th3 = pool.submit(download, datPath, urls[divCount*2:divCount*3])
                    th4 = pool.submit(download, datPath, urls[divCount*3:divCount*4])
            
                pool.shutdown(wait=True)



