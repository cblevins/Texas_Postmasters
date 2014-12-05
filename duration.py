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

print __name__
if __name__ == "__main__":
	PM = getLinesCSV("data/postmasters.csv")
	PO = getLinesCSV("data/Texas_PostOffices.csv")
	M = officeNameMap(PO)
	#add a list of post masters to each post office
	for po in PO:
		if po["FormerName1"] not in ["",po["EarliestName"]]:
			print po
		po["Postmasters"] = []
		
	for pm in PM:
		try:
			ind = M[pm["Office"]]
		except KeyError:
			continue
		PO[ind]["Postmasters"].append(pm)
