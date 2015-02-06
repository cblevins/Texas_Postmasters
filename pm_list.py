from utils import *

def getDurations():
	PM = getLinesCSV("Data/postmasters.csv")

	newPM = []
	testset = set()
	for pm in PM:
		if (pm["Last"]+pm["First"]+pm["Office"]+pm["Year"]) not in testset:
			newPM.append(pm)
			testset.add(pm["Last"]+pm["First"]+pm["Office"]+pm["Year"])
	PM = newPM


	PM = changeFormat(PM)
	print "Number of postmasters: ",
	print len(PM)
	PMlist = []
	RowMap = {}
	for pm in PM:
		try:
			row = RowMap[pm["Office"]+pm["County"]]
			PMlist[row].append(pm)
		except KeyError:
			row = len(PMlist)
			PMlist.append([pm])
			RowMap[pm["Office"]+pm["County"]]=row
	print "Number of offices: ",
	print len(PMlist)

	for pml in PMlist:
		pml = sorted(pml, key = lambda pm : pm["Date"])
		for i in range(len(pml)-1):
			pml[i]["Duration"] = pml[i+1]["Date"]-pml[i]["Date"]
		pml[len(pml)-1]["Duration"] = datetime.timedelta(10000000)

	PO = getLinesCSV("Data/MergedPostOffices.csv")
	PO = changeDates(PO)
	print "Number of post offices from PO: ",
	print len(PO)

	RowMap = {}
	for i in range(len(PO)):
		for county in [PO[i]["County"+str(j)] for j in range(1,4)]:
			if county == "":
				continue
			RowMap[PO[i]["LatestName"]+county] = i
			RowMap[PO[i]["EarliestName"]+county] = i
			for former_name in [PO[i]["FormerName"+str(k)]for k in range(1,6)]:
				if former_name == "":
					continue
				RowMap[former_name+county] = i

	newPM = []
	for pml in PMlist:
		for pm in pml:
			try:
				row = RowMap[pm["Office"]+pm["County"]]
			except KeyError:
				continue
			dates = getDates(PO[row])
			for field, date in dates:
				if date <= pm["Date"]:
					continue
				if date - pm["Date"] < pm["Duration"]:
					pm["Duration"] = date - pm["Date"]
					break
			newPM.append(pm)
	PM = newPM
	print "Final number of postmasters: ",
	print len(PM)
	return PM

def count_problems (required_county, PM):
	date = datetime.date (1902, 1, 1)

	problems = 0
	avg = 0
	num = 0
	for pm in PM:
		if pm["County"] == required_county and pm["Date"] < date:
			if pm["Duration"] == datetime.timedelta(10000000):
				problems = problems + 1
			elif pm["Duration"] == datetime.timedelta(0):
				print pm
			else:
				num = num + 1
				avg = avg + pm["Duration"].days
	if num == 0:
		avg = -1
	else:
		avg = avg / num
	print "Average: ",
	print avg
	print "Number in County: ",
	print num
	return problems

def tostr(d):
	return str(d.month) + "/" + str(d.day) + "/" + str(d.year)

print __name__
if __name__ == "__main__":
	PM = getDurations ()
	newPM = []
	Inaug = getPresidentsDatetime ()
	PresMap = {}
	for i in range(len(Inaug)):
		PresMap[i] = Inaug[i][0]
	for pm in PM:
		if pm["Duration"] == datetime.timedelta(10000000):
			pm["Duration"] = "na"
			pres = getPres(pm, Inaug)
			pm["AppointingPresidentIndex"] = pres + 1
			pm["AppointingPresident"] = PresMap[pres]
			pm["DismissingPresidentIndex"] = "na"
			pm["DismissingPresident"] = "na"
			pm["EndDate"] = "na"
			pm["Date"] = tostr(pm["Date"])
			continue
		pres = getPres(pm, Inaug)
		pm["AppointingPresidentIndex"] = pres + 1
		pm["AppointingPresident"] = PresMap[pres]
		od = pm["Date"]
		pm["Date"] = pm["Duration"] + pm["Date"]
		pres = getPres(pm, Inaug)
		pm["DismissingPresidentIndex"] = pres + 1
		pm["DismissingPresident"] = PresMap[pres]
		pm["EndDate"] = tostr(pm["Date"])
		pm["Date"] = tostr(od)
		pm["Duration"] = pm["Duration"].days

	fieldnames = "NewApp	Last	Office	Month	County	Year	Day	First".split()
	fieldnames.append("Date")
	fieldnames.append("EndDate")
	fieldnames.append("Duration")
	for s in ["Appointing", "Dismissing"]:
		fieldnames.append(s + "President")
		fieldnames.append(s + "PresidentIndex")
	writeCSVs(PM, "data/PostmastersDuration.csv", fieldnames)
			

def nused ():
	PM = getDurations()
	counties = set()
	for pm in PM:
		counties.add(pm["County"])
	counties = sorted(counties)

	Inaug = getPresidentsDatetime ()
	Durations = []
	for ina in Inaug:
		Durations.append([ina[0],0, 0])

	for pm in PM:
		if pm["Duration"] == datetime.timedelta(10000000):
			continue
		pres = getPres(pm, Inaug)
		if pres != -1:
			Durations[pres][1] = Durations[pres][1] + pm["Duration"].days
			Durations[pres][2] = Durations[pres][2] + 1

	for i in range(len(Durations)):
		if i >= len(Durations) - 3:
			continue
		Durations[i][1] = Durations[i][1] / Durations[i][2]

	print Durations

