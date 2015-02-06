from utils import *
print __name__

def tokenize(s):
	try:
		d = [int(s.split("/")[i]) for i in [2,0,1]]
		print d
		return datetime.date(d[0], d[1], d[2])
	except (ValueError, IndexError):
		return "na"

if __name__ == "__main__":
	PM = getLinesCSV("Data/PostmastersDuration.csv")
	PO = getLinesCSV("Data/MergedPostOffices.csv")
	for po in PO:
		for i in range(1, 9):
			po["Dis"+str(i)] = tokenize(po["Dis"+str(i)])
	POMap = {}
	for po in PO:
                names = []
                for i in range(1, 6):
                        names.append(po["FormerName" + str(i)])
                names.append(po["LatestName"])
                names.append(po["EarliestName"])
		for county in [po["County" + str(i)] for i in range (1, 4)]:
			for name in names:
				POMap[name + county] = po

	for pm in PM:
		try:
			po = POMap[pm["Office"] + pm["County"]]
		except KeyError:
			pm["EndType"] = "na"
			continue
		enddate = tokenize(pm["EndDate"])
		if enddate == "na":
			pm["EndType"] = "na"
			continue
		for i in range(1, 9):
			if po["Dis" + str(i)] == enddate:
				pm["EndType"] = 1
				break
		else:
			pm["EndType"] = 0
	fieldnames = "NewApp    Last    Office  Month   County  Year    Day     First".split()
        fieldnames.append("Date")
        fieldnames.append("EndDate")
        fieldnames.append("Duration")
        for s in ["Appointing", "Dismissing"]:
                fieldnames.append(s + "President")
                fieldnames.append(s + "PresidentIndex")
	fieldnames.append("EndType")
	writeCSVs(PM, "Data/PostMastersAdded.csv", fieldnames)
