from utils import *
#map names to indices for easy searching
def officeNameMap(PO):
	M = {}
	i = 0
	for po in PO:
		M[po["EarliestName"]] = i
		M[po["LatestName"]] = i
		for j in range(1,6):
			M[po["FormerName" + str(j)]] = i
		i = i+1
	return M

def testSet(PO):
	S = set()
	for po in PO:
		if getpoyear(po, "Est1") == -1:
			continue
		if getpoyear(po, "Est1") > 1875:
			continue
		if getpoyear(po, "Dis1") < 1875 and getpoyear(po, "Dis1") != -1:
			continue
		S.add(po["EarliestName"])
		S.add(po["LatestName"])
		for i in range(1, 6):
			S.add(po["FormerName"+str(i)])
	return S

def getYears(posplit):
	Years = set()
	for i in range(1, len(posplit)):
		if posplit[i]["End"] == "":
			for j in range(posplit[i]["Start"].year, 1951):
				Years.add(j)
		else:
			for j in range(posplit[i]["Start"].year, posplit[i]["End"].year):
				Years.add(j)
	return Years

print __name__
if __name__ == "__main__":
	PM = getLinesCSV("data/postmasters.csv")
	PO = getLinesCSV("data/Texas_PostOffices.csv")
	print "Entries before dates extracted: " + str(len(PO))

	S = testSet(PO)
	PO = changeDates(PO)


	splitPO = splitPO(PO)
	numPO = {}
	TotalNum = 0

	for posplit in splitPO:
		for i in range(1, len(posplit)):
			if posplit[i]["Start"].year > 1875:
				continue
			if posplit[i]["End"] != "" and posplit[i]["End"].year < 1875:
				continue
			TotalNum = TotalNum + 1
			if posplit[i]["Name"] not in S:
				print posplit
			break
	print TotalNum
#	for posplit in splitPO:
#		Years = getYears(posplit)
#		for County in posplit[0].values():
#			if County not in numPO.keys():
#				numPO[County] = {}
#			for year in Years:
#				if year not in numPO[County].keys():
#					numPO[County][year] = 0
#				numPO[County][year] = numPO[County][year] + 1
#		for year in Years:
#			print year,
#			if year not in TotalNum.keys():
#				TotalNum[year] = 0
#			TotalNum[year] = TotalNum[year] + 1
#		print ""
#	print "Total Num: ",
#	print TotalNum
	M = splitMap(splitPO)

	L = {}
	PM = changeFormat(PM)

	for pm in PM:
		if pm["Office"] + "/" + pm["County"] in L.keys():
			L[pm["Office"] + "/" + pm["County"]].append(pm)
		else:
			L[pm["Office"] + "/" + pm["County"]] = [pm]
	

