import csv

def csv_reader(file_obj):
	reader = csv.DictReader(file_obj)
	return reader

def date(pm):
	s = pm["Month"]
	s += "/"
	s += pm["Day"]
	s += "/"
	s += pm["Year"]
	return s

def check_date(pm, po):
	if date(pm) == po["Est1"] or date(pm) == po["Est2"] or date(pm) == po["Est3"] or date(pm) == po["Est4"] or date(pm) == po["Est5"] or date(pm) == po["Est6"] or date(pm) == po["Est7"] or date(pm) == po["Est8"]:
		return 1
	else:
		return 0

def check_name(pm, po):
	if pm["County"] != po["County1"] and pm["County"] != po["County2"] and pm["County"] != po["County3"]:
		return 0
	if pm["Office"] == po["LatestName"] or pm["Office"] == po["EarliestName"] or pm["Office"] == po["FormerName1"] or pm["Office"] == po["FormerName2"] or pm["Office"] == po["FormerName3"] or pm["Office"] == po["FormerName4"] or pm["Office"] == po["FormerName5"]:
		return 1
	return 0

print(__name__)
if __name__== "__main__":
	PO = []
	PM = []
	po_path = "data/Texas_PostOffices.csv"
	pm_path = "data/Texas_Postmasters.csv"
	with open(po_path, "rU") as f_obj1, open(pm_path, "rU") as f_obj2:
		po_reader = csv_reader(f_obj1)
		pm_reader = csv_reader(f_obj2)
		for row in po_reader:
			PO.append(row)
		for row in pm_reader:
			PM.append(row)

	for pm in PM:
		pm["NewApp"] = -1
		if pm["Last"] == "Pendleton" and pm["First"] == "Geo. C.":
			print pm["Last"],
			print pm["First"]
			i = 0
			for po in PO:
				if check_name(pm, po) == 1:
					print "found"
					print check_date(pm, po)

	for pm in PM:
		for po in PO:
			if check_name(pm, po) == 1:
				pm["NewApp"] = check_date(pm, po)
				break

	for pm in PM:
		if pm["NewApp"] == -1:
			print pm["First"],
			print ' ',
			print pm["Last"]
