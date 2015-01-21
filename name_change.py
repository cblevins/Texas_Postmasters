from utils import *
import operator

def ds (po, field):
	return str(po[field].month) + "/" + str(po[field].day) + "/" + str(po[field].year)

def datestring (po):
	for i in range(1, 6):
		if po["NameChangeDate" + str(i)] != "":
			po["NameChangeDate" + str(i)] = ds(po, "NameChangeDate" + str(i))
	for i in range(1, 9):
		if po["Est" + str(i)] != "":
			po["Est" + str(i)] = ds(po, "Est" + str(i))
		if po["Dis" + str(i)] != "":
			po["Dis" + str(i)] = ds(po, "Dis" + str(i))

def merge (po1, po2):
	if po1["Est1"] < po2["Est1"]:
		parent = po1
		child = po2
	else:
		parent = po2
		child = po1
	newpo = {}
	newpo["EarliestName"] = parent["EarliestName"]
	newpo["LatestName"] = child["LatestName"]
	i = 0
	for county in list(parent["Counties"] | child["Counties"]):
		i = i + 1
		newpo["County" + str(i)] = county
		if i == 3:
			break
	while i < 3:
		i = i + 1
		newpo["County" + str(i)] = ""
	newpo["FormerName1"] = child["EarliestName"]
	newpo["NameChangeDate1"] = child["Est1"]
	newpo["Est1"] = parent["Est1"]
	ED = estDates(parent) | estDates(child)
	ED.discard(parent["Est1"])
	ED.discard(child["Est1"])
	ED.discard("")
	ed = sorted(ED)
	add = 7 - len(ed)
	for i in range(add):
		ed.append("")
	for i in range(0, 7):
		newpo["Est" + str(i+2)] = ed[i]
	DD = disDates(parent) | disDates(child)
	DD.discard("")
	dd = sorted(DD)
	add = 8 - len(dd)
	for i in range(add):
		dd.append("")
	for i in range(8):
		newpo["Dis" + str(i+1)] = dd[i]

	for i in range(2, 6):
		if child["NameChangeDate" + str(i-1)] != "":
			newpo["NameChangeDate" + str(i)] = child["NameChangeDate" + str(i-1)]
			newpo["FormerName" + str(i)] = child["FormerName" + str(i-1)]
		else:
			newpo["NameChangeDate" + str(i)] = newpo["FormerName" + str(i)] = ""
	return newpo

def disDates(po):
        return set(po["Dis" + str(i)] for i in range(1, 9))


def estDates(po):
	return set(po["Est" + str(i)] for i in range(1, 9))

def names(po):
	Names = set(po["FormerName" + str(i)] for i in range(1, 6))
	Names.add(po["LatestName"])
	Names.add(po["EarliestName"])
	Names.discard("")
	return Names

def counties(po):
	Counties = set(po["County" + str(i)] for i in range(1, 4))
	Counties.discard("")
	return Counties

print __name__
if __name__ == "__main__":
	PO = changeDates(getLinesCSV("data/Texas_PostOffices.csv"))
	print len(PO)

	for po in PO:
		for former_name in [po["FormerName" + str(i)] for i in range(1, 6)]:
			if former_name != "":
				po["used"] = -1
				break
		else:
			po["used"] = 0

	for po in PO:
		po["Names"] = names(po)
		po["Counties"] = counties(po)

	mergedPOs = []

	problems = 0

	for i in range(len(PO)):
		cpo = PO[i]
		if cpo["used"] != -1:
			continue
		for j in range(len(PO)):
			po = PO[j]
			if cpo["Names"].isdisjoint(po["Names"]) or cpo["Counties"].isdisjoint(po["Counties"]) or cpo is po:
				continue
			if po["used"] == 1:
				continue
			problems = problems + 1
			mergedPOs.append(merge(cpo, po))
			po["used"] = cpo["used"] = 1
			break

	M = []
	for po in PO:
		if po["used"] != 1:
			del po["used"]
			del po["Counties"]
			del po["Names"]
			M.append(po)

	for po in mergedPOs:
		M.append(po)

	for po in M:
		datestring(po)


	M = sorted(M, key=operator.itemgetter("County1", "LatestName"))
	writeCSV(M, "testing.csv")
	print len(M)
