import enum

# here is the generic type
# we use this as a placeholder if needing to pass values we dont know yet

class L1(enum.Enum):
    FULL_DISK = "XXX"
    COUNTRY = "ligma"
    MESOSCALE = "small area"
    TIME_SCALE = [0, 10, 20, 30, 40, 50]
    ENCODER_TYPE = "HRIT"
    R_CHANNEL = "B03" 
    G_CHANNEL = "B02"
    B_CHANNEL = "B01"
    IR_CHANNEL = "B16"
    QUE_DEPTH = 4
    
class L2(enum.Enum):
    CLOUDS = "sasd"
    MOISTURE = "abc123"
    WIND = "cscsaca"
    TIME_SCALE = [0, 10, 20, 30, 40, 50]


class satellite:
    def __new__(self, cls): # type: ignore
        try:
            return cls.value
        except:
            return cls
    
    def getAttributes(): # type: ignore
        return attrib
    
    IS_REAL = False
    IS_DAY_NUM = False


class attrib(satellite):
    L1 = L1
    L2 = L2
    S3_SOURCE_PATH = "yourmum"
    TIME_SCALE = [0, 10, 20, 30, 40, 50]
    RAW_DATA_COUNT = 160
    GZ_WRAPPED = True

