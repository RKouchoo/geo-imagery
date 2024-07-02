import enum

# WIP!
# this is the goes configuration on S3
# more info will be added for image correction etc

class _goe_L1(enum.Enum):
    FULL_DISK = "AHI-L1b-FLDK"
    JAPAN = "AHI-L1b-Japan"
    MESOSCALE = "AHI-L1b-Target"
    TIME_SCALE = [0, 10, 20, 30, 40, 50]


class _goe_L2(enum.Enum):
    CLOUDS = "AHI-L2-FLDK-Clouds"
    MOISTURE = "AHI-L2-FLDK-ISatSS"
    WIND = "AHI-L2-FLDK-Winds"
    TIME_SCALE = [0, 10, 20, 30, 40, 50]


# lets declare info about goes-16
class attrib:
    S3_SOURCE_PATH = "noaa-goes-16"
    L1 = _goe_L1
    L2 = _goe_L2
    RAW_DATA_COUNT = 160

class satellite:
    def __new__(self, cls):
        return cls.value
    
    IS_REAL = True