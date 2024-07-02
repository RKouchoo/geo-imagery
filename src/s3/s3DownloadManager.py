import bz2
import s3fs
import glob
import os
import time

from sats import satellites
from . import s3DateCarrier
from . import s3DateUtil


import concurrent.futures


# lets init the s3 connector as we will need it while this class is alive
fs = s3fs.S3FileSystem(anon=True)

# Download manager
# I set generic values here so its easier for autocompletion
def  getLatestDataFromS3(queryUrl, 
                         saTime=s3DateCarrier.carrier(None, None, None, None), 
                         satellite=satellites.GENERIC, 
                         ):

    attribs = satellite.getAttributes()

    # check if args were handed in correctly
    if satellite.IS_REAL == False:
        return 0

    # lets check if the time was passed in 
    # we need the time key for saving the data in the right folders
    if saTime.year == None:
        saTime = s3DateUtil.getHimawariLatestDate(attribs.TIME_SCALE)

    # lets generate the gz and dat path
    gzPath = "../data/gz/{}/{}/".format(attribs.S3_SOURCE_PATH, saTime.getCompleteDateString()) 
    datPath = "../data/processed/{}/{}/".format(attribs.S3_SOURCE_PATH, saTime.getCompleteDateString())

    # lets check to see if the data is now there
    notValid = True
    retryCount = 0
    while notValid:
        retryCount += 1
        try:
            files = fs.ls(queryUrl, refresh=True)
            notValid = False
        except:
            print("S3 Query is not ready! {} count: {}".format(queryUrl, retryCount))
            time.sleep(5)

    # lets make sure all the data is there
    files = fs.ls(queryUrl, refresh=True)
    while len(files) != attribs.RAW_DATA_COUNT:
        files = fs.ls(queryUrl, refresh=True)
        print("S3 file count for {} is {} of {}".format(queryUrl, len(files), attribs.RAW_DATA_COUNT))
        time.sleep(1)
    

    # lets create/check for a folder with the UNC name for the files
    if not os.path.exists(gzPath):
        os.makedirs(gzPath)

    if not os.path.exists(datPath):
        os.makedirs(datPath)


    # now that all the checks are finally fucking done
    s3GZfiles = fs.ls(queryUrl, refresh=True)

    # lets split all the files into 4 chunks for a 4 threadded download and extract
    divCount = int(len(s3GZfiles) / 4)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        th1 = pool.submit(threaddedDeX, gzPath, datPath, s3GZfiles[:divCount])
        th2 = pool.submit(threaddedDeX, gzPath, datPath, s3GZfiles[divCount:divCount*2])
        th3 = pool.submit(threaddedDeX, gzPath, datPath, s3GZfiles[divCount*2:divCount*3])
        th4 = pool.submit(threaddedDeX, gzPath, datPath, s3GZfiles[divCount*3:divCount*4])

    # append all the paths into a single place 

    gzfPaths = []
    gzfPaths += th1.result() + th2.result() + th3.result() + th4.result() 


# takes both paths and an array of files in s3
# downloads then extracts the files 
def threaddedDeX(gzpath, datpath, files):
   newpath = []
   
   for gzf in files:
        fs.download(gzf, gzpath+gzf[-47:])
        thePath = gzpath+gzf[-47:]
        newpath.append(thePath)
        print("Downloaded s3 raw: {}".format(gzf))

        gzFile = bz2.BZ2File(thePath)
        gzData = gzFile.read()
        gzs = gzf.split("/")
        gzn = gzs[len(gzs) - 1]
        open(datpath + gzn[:-4], "wb").write(gzData)
        print("Wrote DAT file: {}".format(datpath + gzf[8:-4]))

   return newpath



# checks if the s3 data is there and all intact before we run our ops
def queryS3FilesCorrect(querypath, filecount):
    s3s = s3fs.S3FileSystem(anon=True)
    notValid = True
    fileList = []

    while notValid:
        try:
            files = s3s.ls(querypath, refresh=True)

            while len(files) != filecount:
                files = s3s.ls(querypath, refresh=True)
                s3s.clear_instance_cache()
                time.sleep(1)
            notValid = False
            break
        except:
            print("S3 path not ready!")
        
    return True
