import datetime
import numpy as np
from datetime import date, timedelta, timezone

from . import s3DateCarrier 

# generate a array with the correct formatting for himawari s3
# int timestep to determine which time slot we are looking at, default is 10 mins
# returns s3DateCarrier 
def getLatestDateCarrier(timestep=10):
    time = datetime.datetime.now(timezone.utc) # updated as datetime.UTC() is depriciated
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
    
    return s3DateCarrier.carrier(year, month, day, hours, True)



# jump back to the previous timestamp if the current one is too far ahead
def jumpBack(currentCarrier):

    year = currentCarrier.getYear()
    month = currentCarrier.getMonth()

    day = int(currentCarrier.getDay())
    hours = int(currentCarrier.getTime())

    # check if its midnight, to go back further
    if hours == 0:
        hours = 50
        day -= 1

    day = confine(day)
    hours = confine(hours)

    return s3DateCarrier.carrier(year, month, day, hours, False)


def createCarrierFromURI(URI):

    splt = URI.split("/")
    l = len(splt)

    # check if we have a URI that uses day number 
    if l == 5:
        # lets get the correct month and day from daynum
        start = date(int(int(splt[2])), 1, 1)
        final = start + timedelta(days=int(splt[3]) - 1)
        carr = s3DateCarrier.carrier(splt[2], final.month, final.day,  splt[4] + "00", True)
        carr.setQueryType(True)
    else:
        carr = s3DateCarrier.carrier(splt[2], splt[3], splt[4],  splt[5], False)
        
    carr.setIsGenerated(False)
    carr.setQueryURI(URI)
    return carr


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
    return max(0, ((minute + 5) // 10) * 10 - 10)
