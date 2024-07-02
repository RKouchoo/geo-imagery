import enum

# this is the himawari configuration on S3
# more info will be added for image correction etc

class L1(enum.Enum):
    FULL_DISK = "AHI-L1b-FLDK"
    JAPAN = "AHI-L1b-Japan"
    MESOSCALE = "AHI-L1b-Target"
    ENCODER_TYPE = "ahi_hsd"
    R_CHANNEL = "B03" 
    G_CHANNEL = "B02"
    B_CHANNEL = "B01"
    IR_CHANNEL = "B16"
    
    

class L2(enum.Enum):
    CLOUDS = "AHI-L2-FLDK-Clouds"
    MOISTURE = "AHI-L2-FLDK-ISatSS"
    WIND = "AHI-L2-FLDK-Winds"
    


class satellite:
    IS_REAL = True

    def __new__(self, cls):
        try:
            return cls.value
        except:
            return cls

    
    def getAttributes():
        return attrib
    
    def decodeHelper(self, ok):
        return satellite(ok)


# lets declare info about himawari-9
class attrib:
    L1 = L1
    L2 = L2
    S3_SOURCE_PATH = "noaa-himawari9"
    TIME_SCALE = [0, 10, 20, 30, 40, 50]
    RAW_DATA_COUNT = 160
    GZ_WRAPPED = True
