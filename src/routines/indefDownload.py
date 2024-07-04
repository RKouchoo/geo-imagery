from src.remote import queryStringBuilder
from src.remote import downloadManager
from src.sats import satellites

#sys.path.insert(0, "./")


himawarisat = satellites.HIMAWARI_9
attribs = himawarisat.getAttributes()

while True:
	uri = queryStringBuilder.buildLatestS3QueryURI(sat=himawarisat, prod=attribs.L1.FULL_DISK) # type: ignore
	ags = downloadManager.getLatestDataFromS3(uri.getQueryURI(), saTime=uri, satellite=himawarisat) # type: ignore

