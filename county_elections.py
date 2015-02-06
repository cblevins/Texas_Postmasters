from utils import *
def tokenize(s):
        try:
                d = [int(s.split("/")[i]) for i in [2,0,1]]
                print d
                return datetime.date(d[0], d[1], d[2])
        except (ValueError, IndexError):
                return "na"
print __name__
if __name__ == "__main__":
	PM = getLinesCSV("data/PostmastersPG.csv")
	E = getLinesCSV("data/TexasElections1876-1896.csv")
	Dates = {"1876" : [1876, 11, 1], "1878" : [1876, 11, 5], "1880" : [1880, 11, 2], "1882" : [1882, 11, 7], "1884" : [1884, 11, 4], "1886" : [1886, 11, 2], "1888" : [1888, 11, 6], "1890" : [1890, 11, 4], "1892" : [1892, 11, 8], "1894" : [1894, 11, 8], "1896" : [1896, 11, 3]}
	newPM = []
	for pm in PM:
		pm["Date"] = tokenize(pm["Date"])
		pm["EndDate"] = tokenize(pm["EndDate"])
		if "na" in [pm["Date"], pm["EndDate"]]:
			continue
		if pm["Date"] > datetime.date(1876, 11, 7) and pm["Date"] <= datetime.date(1898, 11, 8):
			newPM.append(pm)
	PM = newPM
	for election in E:
		election["date"] = datetime.date(Dates[election["year"]][0], Dates[election["year"]][1], Dates[election["year"]][2])
	EMap = {}
	for election in E:
		election["county_name"] = election["county_name"].lower()
		if election["county_name"] in EMap.keys():
			EMap[election["county_name"]].append(election)
		else:
			EMap[election["county_name"]] = [election]
	for county in EMap.keys():
		EMap[county] = sorted(EMap[county], key=lambda election: election["date"])
	newPM = []
	for pm in PM:
		try:
			EBlock = EMap[pm["County"].lower()]
		except KeyError:
			continue
		for i in range(1, len(EBlock)):
			if pm["Date"] < EBlock[i]["date"]:
				print EBlock[i]["date"]
				pm["AppCongressionalElection"] = EBlock[i-1]["cong_county_share"]
				pm["AppPresidentialElection"] = EBlock[i-1]["pres_county_share"]
				break
		for i in range(len(EBlock)-1, -1, -1):
			if pm["EndDate"] >= EBlock[i]["date"]:
				pm["DisCongressionalElection"] = EBlock[i]["cong_county_share"]
				pm["DisPresidentialElection"] = EBlock[i]["pres_county_share"]
				break
		newPM.append(pm)
	PM = newPM
	fieldnames = "EndType NewApp	Last	Office	Month	County	Year	Day	First".split()
	fieldnames.append("Date")
	fieldnames.append("EndDate")
	fieldnames.append("Duration")
	for s in ["Appointing", "Dismissing"]:
		fieldnames.append(s + "President")
		fieldnames.append(s + "PresidentIndex")
		fieldnames.append(s + "PG")
		fieldnames.append(s + "PGIndex")
	for s in ["App", "Dis"]:
		fieldnames.append(s + "CongressionalElection")
		fieldnames.append(s + "PresidentialElection")
	writeCSVs(PM, "data/PostmastersElections.csv", fieldnames)

