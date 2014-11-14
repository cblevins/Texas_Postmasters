import csv
def getLines(s):
	f_obj = open(s)
	lines = f_obj.readlines()
	f_obj.close()
	return lines

def getLinesCSV(s,f):
	lines = []
	with open(s,f) as csvfile:
        	reader = csv.DictReader(csvfile)
		for row in reader:
			lines.append(row)
        return lines

def cleanPM(PM):
	PMnew = []
	for pm in PM:
		if pm["Year"] in [""]:
			continue
		PMnew.append(pm)
	return PMnew

def writeCSV(Obj,s):
	fieldnames = Obj[0].keys()
	f_obj = open(s,"wb")
	writer = csv.DictWriter(f_obj, delimiter=',',fieldnames=fieldnames);
	f = dict(zip(fieldnames,fieldnames))
        writer.writerow(f)
	for row in Obj:
		writer.writerow(row)
	f_obj.close()
