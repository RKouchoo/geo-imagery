# data helper for s3 dates, they get poked alot and this makes it easier 
# to be serialised with a dataset in storage

from datetime import date


class carrier:

    year = ""
    month = ""
    day = ""
    time = ""
    generated = False
    numDay = False

    query = ""

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, year, month, day, time, generated): 
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.generated = generated

        return None

    def setQueryURI(self, q):
        self.query = q 

    def getQueryURI(self):
        return self.query
    
    def setQueryType(self, isDay):
        self.numDay = isDay

    def getIsGenerated(self):
        return self.generated
    
    def setIsGenerated(self, gener):
        self.generated = gener

    def getQueryType(self):
        return self.numDay

    def getYear(self):
        return self.year
        
    def getMonth(self):
        return self.month
        
    def getDay(self):
        return self.day
    
    def getTime(self):
        return self.time
    
    def getHour(self):
        return self.time[:2] # 4 digit hour concat to string

    def getDayEpoch(self):
        return date(int(self.year), int(self.month), int(self.day)).timetuple().tm_yday

    def getCompleteDateString(self):
        return self.year + self.month + self.day + self.time
    
    def getStdQueryString(self):
        return "{}/{}/{}/{}".format(self.year, self.month, self.day, self.time)


    
