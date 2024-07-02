import bz2
import s3fs
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
    s3Files = fs.ls(queryUrl, refresh=True)

    # we check if it is even for correct thread handling
    if (int(len(s3Files)) % 2) == 0: 
        
        # lets split all the files into 4 chunks for a 4 threadded download and extract
        divCount = int(len(s3Files) / 4)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            th1 = pool.submit(downloadWrapper, attribs.GZ_WRAPPED, gzPath, datPath, s3Files[:divCount])
            th2 = pool.submit(downloadWrapper, attribs.GZ_WRAPPED, gzPath, datPath, s3Files[divCount:divCount*2])
            th3 = pool.submit(downloadWrapper, attribs.GZ_WRAPPED, gzPath, datPath, s3Files[divCount*2:divCount*3])
            th4 = pool.submit(downloadWrapper, attribs.GZ_WRAPPED, gzPath, datPath, s3Files[divCount*3:divCount*4])
    
        pool.shutdown(wait=True)

        # append all the paths into a single place 
        gzfPaths = []
        gzfPaths += th1.result() + th2.result() + th3.result() + th4.result()

        return [gzfPaths, saTime]
    
    # run in single threadded as there is an odd file count
    # check if there is a need to do gz extraction
    if attribs.GZ_WRAPPED:
        gzfPaths = []

        for gzf in s3Files:
            fs.download(gzf, gzPath+gzf[-47:])
            gzfPaths.append(gzPath+gzf[-47:])
            print("Downloaded s3 raw: {}".format(gzf))

        # lets now extract the dat files from the bz files and put them in the correct folder
       
        for gz in gzfPaths:
            gzFile = bz2.BZ2File(gz)
            gzData = gzFile.read()
            
            wba = gz.split("/")
            fn = wba[len(wba) - 1][:-4]
            open(datPath + fn, "wb").write(gzData)
            print("Wrote dat file: {}".format(datPath + fn))

    else:
        return [doDownload(datPath, s3Files), saTime]




# takes both paths and an array of files in s3
# downloads then extracts the files 
def doDownloadExtract(gzpath, datpath, files):
   newpath = []
   
   for gzf in files:
        fs.download(gzf, gzpath+gzf[-47:])
        thePath = gzpath+gzf[-47:]
        newpath.append(thePath)
        print("Downloaded s3 raw: {}".format(gzf))

        gzFile = bz2.BZ2File(thePath)
        gzData = gzFile.read()
        gzs = gzf.split("/")
        gzn = gzs[len(gzs) - 1][:-4]
        open(datpath + gzn, "wb").write(gzData)
        print("Wrote DAT file: {}".format(datpath + gzn))

   return newpath


# just download the file
def doDownload(rawpath, files):
    paths = []
    for fi in files:
        fs.download(fi, rawpath+fi[-47:])
        paths.append(rawpath+fi[-47:])
        print("Downloaded s3 raw: {}".format(fi))
    return paths


# if the files are GZ wrapped, we can switch between them
def downloadWrapper(isGzWrapped, gzpath, datpath, files):
    if isGzWrapped:
        return doDownloadExtract(gzpath, datpath, files)
    return doDownload(datpath, files)


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
