# data helper for s3 dates, they get poked alot and this makes it easier 
# to be serialised with a dataset in storage

class carrier:

    year = 0
    month = 0
    day = 0
    time = 0
    date = [year, month, day, time]

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, year, month, day, time): 
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.date = [year, month, day, time]
        return None


    def getYear(self):
        return self.year
        
    def getMonth(self):
        return self.month
        
    def getDay(self):
        return self.day
    
    def getTime(self):
        return self.time
        
    def getDateArray(self):
        return self.date

    def getCompleteDateString(self):
        return self.year + self.month + self.day + self.time
