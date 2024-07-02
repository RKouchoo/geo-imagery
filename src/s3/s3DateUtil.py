import datetime
import numpy as np

from . import s3DateCarrier 

# generate a array with the correct formatting for himawari s3
# int timestep to determine which time slot we are looking at, default is 10 mins
# returns s3DateCarrier 
def getHimawariLatestDate(clampWindow, timestep=10):
    time = datetime.datetime.now(datetime.UTC) # updated as datetime.UTC() is depriciated
    year = str(time.year)
    month = confine(time.month)
    day = confine(time.day)
    firstHours = confine(time.strftime("%H")) 
    currentMins = time.minute

    # check if we are going to use a valid s3 time, then clamp it to the correct range 
    if timestep == 10:
        hours = firstHours + confine(str(confineMinsPrevTen(currentMins)))
    else:
        hours = firstHours + str(currentMins)
    
    return s3DateCarrier.carrier(year, month, day, hours)


# confine values the himwari S3 UNC
# converts "6" into "06"
def confine(num):
    newstr = str(num)
    if len(newstr) == 1:
        finalstr = "0" + newstr
        return finalstr
    return newstr


# confine mins to the himwari S3 time entries from an array
# will always default to the lower value e.g time is 1209 it will go to 1200
def confineMins(windowArray, inMins):
    windowArray = np.asarray(windowArray)
    idx = (np.abs(inMins - windowArray )).argmin()
    l = len(windowArray)

    if windowArray[idx] == inMins:
        return windowArray[idx-1]
    elif windowArray[l-1] - inMins < 0:
        return windowArray[l-2]
    elif windowArray[idx] - inMins < 0:
        return windowArray[idx]
    else:
        return windowArray[abs(idx-1)]


def confineMinsPrevTen(minute):
    return ((minute + 5) // 10) * 10 - 10
