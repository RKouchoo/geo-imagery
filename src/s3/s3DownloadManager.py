import bz2
import s3fs
import glob
import os
import time

from sats import satellites
from . import s3DateCarrier
from . import s3DateUtil

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
   
    # lets create/check for a folder with the UNC name for the files
    if not os.path.exists(gzPath):
        os.makedirs(gzPath)

    if not os.path.exists(datPath):
        os.makedirs(datPath)

    # lets check to see if the data is now there
    notValid = True
    nov = 0
    while notValid:
        nov += 1
        try:
            files = fs.ls(queryUrl, refresh=True)
            notValid = False
        except:
            print("S3 Query is not ready! {} count: {}  ".format(queryUrl, nov))
            time.sleep(5)

    # lets make sure all the data is there

    files = fs.ls(queryUrl, refresh=True)
    while len(files) != attribs.RAW_DATA_COUNT:
        files = fs.ls(queryUrl, refresh=True)
        print("S3 file count for {} is {} of {}".format(queryUrl, len(files), attribs.RAW_DATA_COUNT))
        time.sleep(1)
    
    # now that all the checks are finally fucking done
    s3GZfiles = fs.ls(queryUrl, refresh=True)
    
    for gzf in s3GZfiles:
        fs.download(gzf, gzPath+gzf[-47:])
        print("Downloaded s3 raw: {}".format(gzf))

    
    # lets now extract the dat files from the bz files and put them in the correct folder
    localGZFiles = glob.glob(gzPath +"*")
    for gz in localGZFiles:
        print(gz)
        gzFile = bz2.BZ2File(gz)
        gzData = gzFile.read()
        open(datPath + gz[8:-4], "wb").write(gzData)
        print("Wrote dat file: {}".format(datPath + gz[8:-4]))



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






'''

'''