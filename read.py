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
        for po in PO:
		print po["LatestName"]
		for pm in PM:
			if pm["Office"] == po["LatestName"] and date(pm) == po["Est1"]:
				print pm["First"] + " " + pm["Last"]
				print "Est: " + po["Est1"]
