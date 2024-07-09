

import os
import glob 


import os
# get the file name list to nameList
nameList = glob.glob("*.png")
#loop through the name and rename

i = 1

for fileName in nameList:
    rename="himawari_{}.png".format('%04d' % i)
    os.rename(fileName,rename)
    i+=1
#example:
#input fileName bulk like :20180707131932_IMG_4304.JPG
#output renamed bulk like :IMG_4304.JPG
