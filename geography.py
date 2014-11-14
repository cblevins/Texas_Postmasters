from utils import *

def locationMap(POLocation):
	LM = {}
	for po in POLocation:
		LM[po["Post Office"]] = [po["Latitude"],po["Longitude"]]
	return LM

def setLocation(PM,LM):
	for pm in PM:
		try:
			[pm["Latitude"],pm["Longitude"]] = LM[pm["Office"]]
		except KeyError:
			[pm["Latitude"],pm["Longitude"]] = [-1,-1]
	return PM

print __name__
if __name__ == "__main__":
	PM = getLinesCSV("data/newPostmastersmulti.csv", "rU")
	LM = locationMap(getLinesCSV("data/Texas_PostOffices_Coordinates.csv","rU"))
	PM = setLocation(PM,LM)
	writeCSV(PM,"data/Geography/PostmastersWithLocation.csv")
