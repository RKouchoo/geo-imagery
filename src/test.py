
from remote import s3ExtendedUtil
from remote import dateCarrier
from sats import satellites



s3ExtendedUtil.downloadS3BucketDay(dateCarrier.carrier("2026", "05", "04", "0", False), satellites.HIMAWARI_9, satellites.HIMAWARI_9.getAttributes().L1.FULL_DISK, retainGz=False)