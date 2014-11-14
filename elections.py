from utils import *

def makeEMap(e):
	m = {}
	for r in e:
		print r["Dem_Tot"],
		print " ",
		print r["Rep_Tot"]
		m[r["NHGISNAM"]] = [int((r["Dem_Tot"]).replace(",","")),int((r["Rep_Tot"]).replace(",",""))]
	return m

def getElections():
        e1864 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1864_Elections.txt")
        e1868 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1868_Elections.txt")
        e1872 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1872_Elections.txt")
        e1876 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1876_Elections.txt")
        e1880 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1880_Elections.txt")
        e1884 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1884_Elections.txt")
        e1888 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1888_Elections.txt")
        e1892 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1892_Elections.txt")
        e1896 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1896_Elections.txt")
        e1900 = getLinesCSV("data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_1900_Elections.txt")

	Elections = []
	Elections.append(makeEMap(e1864))
	Elections.append(makeEMap(e1868))
	Elections.append(makeEMap(e1872))
	Elections.append(makeEMap(e1876))
	Elections.append(makeEMap(e1880))
	Elections.append(makeEMap(e1884))
	Elections.append(makeEMap(e1888))
	Elections.append(makeEMap(e1892))
	Elections.append(makeEMap(e1896))
	Elections.append(makeEMap(e1900))
	return Elections

def inRange(PM,low,high):
	PMnew = []
	for pm in PM:
		if (int(pm["Year"]) < low) or (int(pm["Year"]) > high):
			continue
		PMnew.append(pm)
	return PMnew

def getElectionYear(ind):
	ElectionYears = [1864,1868,1872,1880,1884,1888,1892,1892,1900]
	return ElectionYears[ind]

def getLastElection(pm):
	ElectionYears = [1864,1868,1872,1880,1884,1888,1892,1892,1900]
	for ey in ElectionYears:
		if int(pm["Year"]) > ey:
			return ElectionYears.index(ey)
	else:
		return -1

def findElections(PM,Elections):
	for pm in PM:
		ind = getLastElection(pm)
		pm["ElectionYear"] = getElectionYear(ind)
		try:
			[pm["Dem_Tot"],pm["Rep_Tot"]] = Elections[ind][pm["County"]]
		except KeyError:
			[pm["Dem_Tot"],pm["Rep_Tot"]] = [-1,-1]
	return PM

print __name__
if __name__ == "__main__":
	Elections = getElections()
	PM = getLinesCSV("data/newPostmastersmulti.csv")
	PM = cleanPM(PM)
	PM = inRange(PM,1864,1900)
	PM = findElections(PM,Elections)
