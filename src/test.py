from remote import s3ExtendedUtil
from remote import dateCarrier
from sats import satellites

from remote import queryStringBuilder
from sats.goesSatellite import satellite

#query1 = queryStringBuilder.buildDayQuery(satellites.HIMAWARI_9, satellites.HIMAWARI_9.getAttributes().L1.FULL_DISK)
#s3ExtendedUtil.downloadS3BucketDay(parentQueryURI=query1, satellite=satellites.HIMAWARI_9, sector=satellites.HIMAWARI_9.getAttributes().L1.FULL_DISK, retainGz=False)

query2 = queryStringBuilder.buildDayQuery(satellites.GOES_19, satellites.GOES_19.getAttributes().L1.FULL_DISK)

s3ExtendedUtil.downloadS3BucketDay(parentQueryURI=query2, satellite=satellites.GOES_19, sector=satellites.GOES_19.getAttributes().L1.FULL_DISK, retainGz=False)