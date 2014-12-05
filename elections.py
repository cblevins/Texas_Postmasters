from utils import *

def makeMap(e):
	m = {}
	for r in e:
		#map county names to results 
		m[r["NHGISNAM"]] = [int((r["Dem_Tot"]).replace(",","")),int((r["Rep_Tot"]).replace(",",""))]
	return m

def getElections():
	#create a map of years to a county-results map
	Elections = {}
	s_left = "data/Texas_Elections_1864-1900/Texas Election Results in CSV/TX_"
	s_right = "_Elections.txt"
	for year in range(1864, 1904, 4):
		#opens the election file for each year and uses it to create a county to results file for that year
		Elections[year] = makeMap(getLinesCSV(s_left + str(year) + s_right))
	return Elections

def getLastElection(p):
	for year in range(1864, 1904, 4):
		if int(p["Year"]) <= year + 3:
			return year
	else:
		return -1 

def findElections(PM,Elections):
	for pm in PM:
		year = getLastElection(pm)
		try:
			[pm["Dem_Tot"],pm["Rep_Tot"]] = Elections[year][pm["County"]]
		except KeyError:
			[pm["Dem_Tot"],pm["Rep_Tot"]] = [-1,-1]
	return PM


#map of national election results: 0-rep, 1-dem
def getNationalResults():
        Results = {}
        for year in range(1864, 1904, 4):
                Results[year] = 0
        Results[1884] = 1
        Results[1892] = 1
	return Results

def findElectionsForCounties(Counties, Elections):
	newCounties = []
	Results = getNationalResults()
	for county in Counties:
		year = getLastElection(county)
		try:
			[county["Dem_Tot"], county["Rep_Tot"]] = Elections[year][county["Name"]]
			if county["Dem_Tot"] == 99989990:
				continue
			if Results[year]==1:
				county["dif"] = county["Dem_Tot"] - county["Rep_Tot"]
			else:
				county["dif"] = county["Rep_Tot"] - county["Dem_Tot"]
			newCounties.append(county)
		except KeyError:
			continue
	return newCounties

print __name__
if __name__ == "__main__":
	set = True
	Elections = getElections()
	Counties = getLinesCSV("data/counties.csv")
	#delete aggregrate county entries
	Counties = cleanCSV(Counties, "Year", ["-", ""])
	Counties = findElectionsForCounties(Counties, Elections)
	print len(Counties)
	Counties = cleanCSV(Counties, "Dem_Tot", [99989990])
	Correlation = []
	count = 0
	for c in Counties:
		Cor = {}
		#dif is votes for national winner - votes for loser
		bin = -1 if c["dif"] < 0 else 1
		if bin == -1:
			count = count + 1
		[Cor["Ratio"],Cor["Dif"]] = [float(1 + int(c["ChangeNum"]))/(1 + int(c["EstNum"])), c["dif"] if set else bin]
		Correlation.append(Cor)
	writeCSV(Correlation, "data/correlation.csv")
	print count
