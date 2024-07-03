import enum

# WIP!
# this is the goes configuration on S3
# more info will be added for image correction etc

# https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi?source=aws&satellite=noaa-goes18
# https://noaa-goes18.s3.amazonaws.com/ABI-L1b-RadM/2024/184/11/

class _goe_L1(enum.Enum):
    FULL_DISK = "ABI-L1b-RadF"
    CONUS = "ABI-L1b-RadC"
    MULTI_MESOSCALE = True
    MESOSCALE = "ABI-L1b-RadM"
    MESOSCALE_EXTENSIONS = ["RadM1", "RadM2"]
    ENCODER_TYPE = "abi"
    QUE_DEPTH = 3
    


class _goe_L2(enum.Enum):
    CLOUDS = "AHI-L2-FLDK-Clouds"
    MOISTURE = "AHI-L2-FLDK-ISatSS"
    WIND = "AHI-L2-FLDK-Winds"


# lets declare info about goes-16
class attrib:
    S3_SOURCE_PATH = "noaa-goes18"
    L1 = _goe_L1
    L2 = _goe_L2
    TIME_SCALE = [0, 10, 20, 30, 40, 50]
    RAW_DATA_COUNT = 96
    IS_DAY_NUM = True

class satellite:
    def __new__(self, cls):
        try:
            return cls.value
        except:
            return cls
    
    def getAttributes():
        return attrib

    IS_REAL = True
    GZ_WRAPPED = False

