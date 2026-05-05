from remote import s3ExtendedUtil
from remote import dateCarrier
from sats import satellites

from remote import queryStringBuilder
from sats.goesSatellite import satellite

#s3ExtendedUtil.downloadS3BucketDay(dateCarrier.carrier("2026", "05", "05", "0", False), satellites.HIMAWARI_9, satellites.HIMAWARI_9.getAttributes().L1.FULL_DISK, retainGz=False)

query2 = queryStringBuilder.buildDayQuery(satellites.GOES_18, satellites.GOES_18.getAttributes().L1.FULL_DISK)

s3ExtendedUtil.downloadS3BucketDay(parentQueryURI=query2, satellite=satellites.GOES_18, sector=satellites.GOES_18.getAttributes().L1.FULL_DISK, retainGz=False)