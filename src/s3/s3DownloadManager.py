import bz2
import s3fs
import glob
import os

from sats import satellites
from . import s3DateCarrier
from . import s3DateUtil

# lets init the s3 connector as we will need it while this class is alive
fs = s3fs.S3FileSystem(anon=True)

# Download manager
# I set generic values here so its easier for autocompletion
def  getLatestDataFromS3(queryUrl, 
                         time=s3DateCarrier.carrier(None, None, None, None), 
                         satellite=satellites.GENERIC, 
                         ):

    attribs = satellite.getAttributes()

    # check if args were handed in correctly
    if satellite.IS_REAL == False:
        return 0

    # lets check if the time was passed in 
    # we need the time key for saving the data in the right folders
    if time.year == None:
        time = s3DateUtil.getHimawariLatestDate(attribs.TIME_SCALE)

    # lets generate the gz and dat path
    gzPath = "../data/gz/{}/{}/".format(attribs.S3_SOURCE_PATH, time.getCompleteDateString()) 
    datPath = "../data/processed/{}/{}/".format(attribs.S3_SOURCE_PATH, time.getCompleteDateString())
   
    # lets create/check for a folder with the UNC name for the raw GZ files
    if not os.path.exists(gzPath):
        os.makedirs(gzPath)

    # lets grab the latest data into the GZ path now
    s3GZfiles = fs.ls(queryUrl)
    for gzf in s3GZfiles:
        fs.download(gzf, gzPath)
        print("Downloaded s3 raw: {}".format(gzf))

    # lets now extract the dat files from the bz files and put them in the correct folder
    localGZFiles = glob.glob(gzPath)
    for gz in localGZFiles:
        gzFile = bz2.BZ2File(gz)
        gzData = gzFile.read()
        open(datPath + gz[8:-4], "wb").write(gzData)
        print("Wrote dat file: {}".format(datPath + gz[8:-4]))


    

    

    




