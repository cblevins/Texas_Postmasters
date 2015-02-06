from utils import *
def tokenize(s):
        try:
                d = [int(s.split("/")[i]) for i in [2,0,1]]
                print d
                return datetime.date(d[0], d[1], d[2])
        except (ValueError, IndexError):
                return "na"

def tostr(d):
        return str(d.month) + "/" + str(d.day) + "/" + str(d.year)

print __name__
if __name__ == "__main__":
	PM = getLinesCSV("data/PostmastersAdded.csv")
	Inaug = getPG()
	for pm in PM:
		pm["Date"] = tokenize(pm["Date"])
		pm["EndDate"] = tokenize(pm["EndDate"])
		if pm["Date"] == "na":
			pm["AppointingPGIndex"] = pm["AppointingPG"] = "na"
		else:
			pm["AppointingPGIndex"] = getPresf(pm, Inaug, "Date")
			pm["AppointingPG"] = Inaug[pm["AppointingPGIndex"]][0]
		if pm["EndDate"] == "na":
                        pm["DismissingPGIndex"] = pm["DismissingPG"] = "na"
                else:
                        pm["DismissingPGIndex"] = getPresf(pm, Inaug, "EndDate")
                        pm["DismissingPG"] = Inaug[pm["DismissingPGIndex"]][0]
	for pm in PM:
		if pm["Date"] != "na":
			pm["Date"] = tostr(pm["Date"])
		if pm["EndDate"] != "na":
			pm["EndDate"] = tostr(pm["EndDate"])

	fieldnames = "EndType NewApp	Last	Office	Month	County	Year	Day	First".split()
	fieldnames.append("Date")
	fieldnames.append("EndDate")
	fieldnames.append("Duration")
	for s in ["Appointing", "Dismissing"]:
		fieldnames.append(s + "President")
		fieldnames.append(s + "PresidentIndex")
		fieldnames.append(s + "PG")
		fieldnames.append(s + "PGIndex")
	writeCSVs(PM, "data/PostmastersPG.csv", fieldnames)
