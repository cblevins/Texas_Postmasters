import copy
import csv
import datetime

def changeFormat(PM):
        newPM = []
        for pm in PM:
                pmDate(pm)
                if pm["Date"] != "":
                        newPM.append(pm)
        return newPM

def pmDate(pm):
	try:
		pm["Date"] = datetime.date(int(pm["Year"]), int(pm["Month"]), int(pm["Day"]))
	except ValueError:
		pm["Date"] = ""
#creates a multi-level map of the split post offices
def splitMap(PO):
	M = {}
	for polist in PO:
		for field,county in polist[0].iteritems():
			if county not in M.keys():
				M[county] = {}
			for i in range(1, len(polist)):
				try:
					M[county][polist[i]["Name"]].append(polist[i])
				except KeyError:
					M[county][polist[i]["Name"]] = [polist[i]]
	return M

#returns list of field, date pairs extracted from a po entry
def getDates(po):
        Dates = []
        for i in range(1,9):
                if po["Est" + str(i)] != "":
                        Dates.append(["Est" + str(i), po["Est" + str(i)]])
        for i in range(1,9):
                if po["Dis" + str(i)] != "":
                        Dates.append(["Dis" + str(i), po["Dis" + str(i)]])
        for i in range(1,6):
                if po["NameChangeDate" + str(i)] != "":
                        Dates.append(["NameChangeDate" + str(i), po["NameChangeDate" + str(i)]])

        Dates = sorted(Dates, key = lambda date: date[1])
	return Dates

#returns date, name pair
def getNames(po, Dates):
        Names = []
        for d in Dates:
                if "NameChangeDate" in d[0]:
                        Names.append([d[1], po["FormerName" + d[0][-1]]])
	return Names

#splits post office entry into a list of easily manipulable post offices. The list has an EarliestName identifier
def splitpo(po):
	Dates = getDates(po)
	Names = getNames(po, Dates)


	polist = []
	#dict of counties
	polist.append(dict(("County"+str(i), po["County"+str(i)]) for i in range(1,4)))

	#iterate through the dates
	for i in range(len(Dates)):
		#search for establishment or name changes
		if "Dis" in Dates[i][0]:
			continue

		#get start and end dates
		start = Dates[i][1]
		if i == len(Dates) - 1:
			end = ""
		else:
			end = Dates[i+1][1]

		#find name
		for j in range(len(Names)):
			if start < Names[j][0] and j != 0:
				name = Names[j-1][1]
				break
		else:
			name = po["EarliestName"]

		polist.append({"Name":name, "Start":start, "End":end})
	return polist

def splitPO(PO):
	newPO = []
	for po in PO:
		newPO.append(splitpo(po))
	return newPO

#convert name fields to lists of ints
def extractDates(po):
	newpo = dict((k,v) for k,v in po.items())
	for i in range(1,9):
		if po["Est" + str(i)] == "":
			newpo["Est" + str(i)] == ""
			continue
		try:
			date = [int(str.split(po["Est" + str(i)],"/")[j]) for j in [2,0,1]]
			newpo["Est" + str(i)] = datetime.date(date[0], date[1], date[2])
		except (ValueError,IndexError):
			raise ValueError("Bad date")
        for i in range(1,9):
                if po["Dis" + str(i)] == "":
                        newpo["Dis" + str(i)] == ""
                        continue
                try:
                        date = [int(str.split(po["Dis" + str(i)],"/")[j]) for j in [2,0,1]]
			newpo["Dis" + str(i)] = datetime.date(date[0], date[1], date[2])
                except (ValueError,IndexError):
                        raise ValueError("Bad date")
        for i in range(1,6):
                if po["NameChangeDate" + str(i)] == "":
                        newpo["NameChangeDate" + str(i)] == ""
                        continue
                try:
                        date = [int(str.split(po["NameChangeDate" + str(i)],"/")[j]) for j in [2,0,1]]
			newpo["NameChangeDate" + str(i)] = datetime.date(date[0], date[1], date[2])
                except (ValueError,IndexError):
                        raise ValueError("Bad date")
	return newpo

def changeDates(PO):
	newPO = []
	for po in PO:
		try:
			newPO.append(extractDates(po))
		except ValueError:
			continue
	return newPO

def getpoyear(po, field):
	try:
		return int(str.split(po[field], "/")[2])
	except (ValueError, IndexError):
		return -1

#maps post office names to coordinates
def locationMap():
	POLocation = getLinesCSV("data/Texas_PostOffices_Coordinates.csv")
        LM = {}
        for po in POLocation:
                LM[po["Post Office"]] = [po["Latitude"],po["Longitude"]]
        return LM

#checks if a postmaster appointment counts as a changeover i.e. NewApp == 0
def isChangeover(pm):
	return pm["NewApp"] == '0'

#removes postmasters who were appointed before or after a certain date
#postmasters appointed on the dates are retained
#dates are in format [y, m, d] e.g. [1992, 6, 5]
#entries with badly formatted dates are removed
def inRange(PM, start, end):
	sd = datetime.date(start[0], start[1], start[2])
	ed = datetime.date(end[0],end[1],end[2])
	PMnew = []
	for pm in PM:
		try:
			d = datetime.date(int(pm["Year"]), int(pm["Month"]),int(pm["Day"]))
		except ValueError:
			continue
		if (d < sd) or (ed < d):
			continue
		PMnew.append(pm)
	return PMnew

#returns true if the first date is less than or equal to the second
#the dates are passed in as tuples
def le(t1,t2):
	d1 = datetime.date(t1[0],t1[1],t1[2])
	d2 = datetime.date(t2[0],t2[1],t2[2])
	return not (d2 < d1)

#returns true if the first date is less than the second
#the dates are passed in as tuples
def l(t1,t2):
        d1 = datetime.date(t1[0],t1[1],t1[2])
        d2 = datetime.date(t2[0],t2[1],t2[2])
        return d1 < d2

#gets lines from a file
def getLines(s):
	f_obj = open(s)
	lines = f_obj.readlines()
	f_obj.close()
	return lines

#gets lines from a file. each line is a dictionary
def getLinesCSV(s,f="rU"):
	lines = []
	with open(s,f) as csvfile:
        	reader = csv.DictReader(csvfile)
		for row in reader:
			lines.append(row)
        return lines

#checks whether a post master worked at a post office by comparing names
def check_name(pm, po):
        if pm["County"] in [po["County1"], po["County2"], po["County3"]]:
                if pm["Office"] in [po["LatestName"], po["EarliestName"], po["FormerName1"], po["FormerName2"], po["FormerName3"], po["FormerName4"], po["FormerName5"]]:
                        return 1;
        return 0;

#converts the three date columns to a single string
def date(pm):
        return (pm["Month"] + "/" + pm["Day"] + "/" + pm["Year"])

#returns the establishment or name change number
def check_date(pm,po):
        d = date(pm)
        for i in range(1,9):
                if d == po["Est" + str(i)]:
                        return i
        for i in range(1,6):
                if d == po["NameChangeDate" + str(i)]:
                        return (-1*i)
        return 0

#deletes csv entries with badly formatted values for a field
#pass in values as a tuple e.g. [1834, 1900] if you field is "Year"
def cleanCSV(Obj, field, values):
	Objnew = []
	for o in Obj:
		if o[field] not in values:
			Objnew.append(o)
	return Objnew

#prints a csv object to a file
def writeCSV(Obj,s):
	fieldnames = "LatestName	EarliestName	County1	County2	County3	Est1	Est2	Est3	Est4	Est5	Est6	Est7	Est8	Dis1	Dis2	Dis3	Dis4	Dis5	Dis6	Dis7	Dis8	NameChangeDate1	FormerName1	NameChangeDate2	FormerName2	NameChangeDate3	FormerName3	NameChangeDate4	FormerName4	NameChangeDate5	FormerName5".split()
	f_obj = open(s,"wb")
	writer = csv.DictWriter(f_obj, delimiter=',',fieldnames=fieldnames);
	f = dict(zip(fieldnames,fieldnames))
        writer.writerow(f)
	for row in Obj:
		writer.writerow(row)
	f_obj.close()
def writeCSVs(Obj, s, fieldnames):
        f_obj = open(s,"wb")
        writer = csv.DictWriter(f_obj, delimiter=',',fieldnames=fieldnames);
        f = dict(zip(fieldnames,fieldnames))
        writer.writerow(f)
        for row in Obj:
                writer.writerow(row)
        f_obj.close()

def tokenizet(s, t):
        try:
                d = [int(s.split(t)[i]) for i in [0,1,2]]
                return datetime.date(d[0], d[1], d[2])
        except (ValueError, IndexError):
                return "na"

#returns a list containing the names and innauguration dates of presidents
def getPresidents():
	Inaug = [["Polk",[4,3,1845]], ["Taylor",[5,3,1849]], ["Fillmore",[10,7,1850]], ["Pierce",[4,3,1853]], ["Buchanan",[4,3,1857]], ["Lincoln1",[4,3,1861]], ["Lincoln2",[4,3,1865]], ["Johnson",[15,4,1865]], ["Grant1",[4,3,1869]], ["Grant2",[4,3,1873]], ["Hayes",[5,3,1877]], ["Garfield",[4,3,1881]], ["Arthur",[20,9,1881]], ["Cleveland1",[4,3,1885]], ["Harrison",[4,3,1889]], ["Cleveland2",[4,3,1893]], ["McKinley",[4,3,1897]], ["McKinley",[4,3,1901]], ["Roosevelt1",[14,9,1901]], ["Roosevelt2",[4,3,1905]], ["Taft",[4,3,1909]], ["Wilson1",[4,3,1913]], ["Wilson2",[5,3,1917]], ["Harding",[4,3,1921]], ["Coolidge",[3,8,1923]], ["Hoover",[4,3,1925]], ["F.D.Roosevelt1",[4,3,1929]], ["F.D.Roosevelt2",[4,3,1933]], ["F.D.Roosevelt3",[20,1,1937]], ["Truman",[20,1,1941]]]
	return Inaug

def getPresidentsDatetime():
	Inaug = getPresidents()
	for i in Inaug:
		i[1] = datetime.date(i[1][2],i[1][1],i[1][0])
	return Inaug

def getPresf(pm, Inaug, f):
        for i in range(len(Inaug)):
                if pm[f] < Inaug[i][1]:
                        return i - 1
        else:
                return -1

def getPres(pm, Inaug):
	for i in range(len(Inaug)):
		if pm["Date"] < Inaug[i][1]:
			return i - 1
	else:
		return -1

#maps numbers to names
def getPresidentsMap():
	Inaug = getPresidents()
	M = {}
	for i in range(len(Inaug)):
		M[i] = Inaug[i][0]
	return M

def getPG():
	Inaug = getLinesCSV("data/PostmasterGenerals_dates.csv")
	nInaug = []
	for ina in Inaug:
		nInaug.append([ina["Name"], tokenizet(ina["Date"], "-")])
	print nInaug
	return nInaug

#cycles through presidents and returns the index of the president under whom a postmaster appointment was made
#appointments made under Truman are considered invalid (returns -1)
def getPresidentForpm(pm, Inaug):
	for i in range(len(Inaug)):
		if l([int(pm["Year"]),int(pm["Month"]),int(pm["Day"])],[Inaug[i][1][2],Inaug[i][1][1],Inaug[i][1][0]]):
			return i-1
	return -1
