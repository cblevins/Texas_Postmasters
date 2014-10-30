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

def check_date_multi(pm,po):
	if date(pm) == po["Est1"]:
		return 1
	elif date(pm) == po["Est2"]:
		return 2
	elif date(pm) == po["Est3"]:
		return 3
	elif date(pm) == po["Est4"]:
		return 4
	elif date(pm) == po["Est5"]:
		return 5
	elif date(pm) == po["Est6"]:
		return 6
	elif date(pm) == po["Est7"]:
		return 7
	elif date(pm) == po["Est8"]:
		return 8
	elif date(pm) == po["NameChangeDate1"]:
		return -1
	elif date(pm) == po["NameChangeDate2"]:
                return -2
	elif date(pm) == po["NameChangeDate3"]:
                return -3
	elif date(pm) == po["NameChangeDate4"]:
                return -4
	elif date(pm) == po["NameChangeDate5"]:
                return -5
	else:
		return 0

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
		pm["NewApp"] = -50;

	for pm in PM:
		for po in PO:
			if check_name(pm, po) == 1:
				pm["NewApp"] = check_date_multi(pm, po)
				break

	print i
	print j	
	fieldnames = PM[0].keys()

	new_po_path = "data/newPostmastersmulti.csv"
	f_obj3 = open(new_po_path, "wb")
	pm_writer = csv.DictWriter(f_obj3, delimiter=',',fieldnames=fieldnames);
	f = dict(zip(fieldnames,fieldnames))
	pm_writer.writerow(f)
	for pm in PM:
		pm_writer.writerow(pm)
	f_obj3.close();
