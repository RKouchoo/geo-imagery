from remote import threddsBuilder
from remote import dateCarrier
from remote import downloadManager


datPath = "../data/thredds/"
downloadManager.downloadCompleteThreddsDataset(datPath, threddsBuilder.getThreddsDayCustomURI(dateCarrier.carrier("2026", "02", "16", "00", False)))
#downloadManager.downloadCompleteThreddsDataset(datPath, threddsBuilder.getThreddsDayCustomURI(dateCarrier.carrier("2024", "07", "04", "00", False)))
#downloadManager.downloadCompleteThreddsDataset(datPath, threddsBuilder.getThreddsDayCustomURI(dateCarrier.carrier("2024", "07", "05", "00", False)))