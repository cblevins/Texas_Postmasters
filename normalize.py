import csv
print(__name__)
if __name__ == "__main__":
	f_obj1 = open("data/PostMastersInRange.csv")
	reader = csv.DictReader(f_obj1)

	PM = []
	for row in reader:
		PM.append(row)
	f_obj1.close()
	
	NumOffices = [452,494,489,521,596,654,749,818,861,908,1022,1131,1218,1344,1364,1438,1448,1604,1684,1830,1907,2045,2106,2248,2349,2477,2572,2687,2730,2755,2766,2860,2968,3112,3188,3245]

	for pm in PM:
		ind = int(pm["Year"]) - 1867
		pm["Weight"] = NumOffices[ind]

	Presidents = []
	PresidentsEst = []
	i = 0
	while i < 36:
		Presidents.append(0)
		PresidentsEst.append(0)
		i = i + 1

	for pm in PM:
		ind = int(pm["President"])
		w = 1.0/float(int(pm["Weight"]))
		if pm["NewApp"] == "0":
			Presidents[ind] = Presidents[ind] + w
		else:
			PresidentsEst[ind] = PresidentsEst[ind] + w

	print Presidents
	print PresidentsEst
