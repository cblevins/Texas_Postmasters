import csv
import datetime

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

#deletes postmaster entries with badly formatted dates
def cleanPM(PM):
	PMnew = []
	for pm in PM:
		for pm in PM:
                	if pm["Year"] == "" or pm["Year"] == "0":
                        	continue
                	elif pm["Month"] == "" or pm["Month"] == "0":
                        	continue
                	elif pm["Day"] == "" or pm["Day"] == "0":
                        	continue
			PMnew.append(pm)
	return PMnew

#prints a csv object to a file
def writeCSV(Obj,s):
	fieldnames = Obj[0].keys()
	f_obj = open(s,"wb")
	writer = csv.DictWriter(f_obj, delimiter=',',fieldnames=fieldnames);
	f = dict(zip(fieldnames,fieldnames))
        writer.writerow(f)
	for row in Obj:
		writer.writerow(row)
	f_obj.close()

#returns a list containing the names and innauguration dates of presidents
def getPresidents():
	Inaug = [["Polk",[4,3,1845]], ["Taylor",[5,3,1849]], ["Fillmore",[10,7,1850]], ["Pierce",[4,3,1853]], ["Buchanan",[4,3,1857]], ["Lincoln1",[4,3,1861]], ["Lincoln2",[4,3,1865]], ["Johnson",[15,4,1865]], ["Grant1",[4,3,1869]], ["Grant2",[4,3,1873]], ["Hayes",[5,3,1877]], ["Garfield",[4,3,1881]], ["Arthur",[20,9,1881]], ["Cleveland1",[4,3,1885]], ["Harrison",[4,3,1889]], ["Cleveland2",[4,3,1893]], ["McKinley",[4,3,1897]], ["McKinley",[4,3,1901]], ["Roosevelt1",[14,9,1901]], ["Roosevelt2",[4,3,1905]], ["Taft",[4,3,1909]], ["Wilson1",[4,3,1913]], ["Wilson2",[5,3,1917]], ["Harding",[4,3,1921]], ["Coolidge",[3,8,1923]], ["Hoover",[4,3,1925]], ["F.D.Roosevelt1",[4,3,1929]], ["F.D.Roosevelt2",[4,3,1933]], ["F.D.Roosevelt3",[20,1,1937]], ["Truman",[20,1,1941]]]
	return Inaug

#maps numbers to names
def getPresidentsMap():
	Inaug = getPresidents()
	M = {}
	for i in range(len(Inaug)):
		M[i] = Inaug[i][0]
	return M

#cycles through presidents and returns the index of the president under whom a postmaster appointment was made
#appointments made under Truman are considered invalid (returns -1)
def getPresidentForpm(pm, Inaug):
	for i in range(len(Inaug)):
		if l([int(pm["Year"]),int(pm["Month"]),int(pm["Day"])],[Inaug[i][1][2],Inaug[i][1][1],Inaug[i][1][0]]):
			return i-1
	return -1
